"""Озвучка книги через XTTS-v2.

Поток:
    .txt  --(preprocess)-->  главы  -->  предложения  -->  чанки <=240 симв.
       --(XTTS, voice clone)-->  *.wav (в кеше) -->  склейка через ffmpeg
       --> .m4b с разметкой глав  или  .mp3.

Кеш предложений хранится в <output>.cache/, файлы именуются по sha1 текста и
голосу. Если упало посередине — просто повторите запуск, готовые куски
переозвучивать не будем.

Использование:
    python audio/tts_book.py \
        --input  book.ru.txt \
        --output book.ru.m4b \
        --voice  audio/voices/narrator.wav \
        --accent

Лицензия XTTS-v2 — Coqui Public Model License (некоммерческое использование).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from tqdm import tqdm

# Локальный модуль рядом со скриптом.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from preprocess import normalize, pack_chunks, split_sentences  # noqa: E402


CHAPTER_RE = re.compile(
    r"^\s*(?:Глава|ГЛАВА|Chapter|CHAPTER)\s+[IVXLCDM\d]+[\.\:\s].*$",
    re.MULTILINE,
)


@dataclass
class Chapter:
    title: str
    text: str


def split_chapters(text: str) -> list[Chapter]:
    """Если в книге есть строки вида 'Глава 1' / 'Chapter I' — режем по ним.
    Иначе считаем весь текст одной главой."""
    matches = list(CHAPTER_RE.finditer(text))
    if not matches:
        return [Chapter(title="Книга", text=text)]
    chapters: list[Chapter] = []
    for i, m in enumerate(matches):
        title = m.group(0).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body:
            chapters.append(Chapter(title=title, text=body))
    return chapters


def sentence_hash(text: str, voice_path: str, language: str) -> str:
    h = hashlib.sha1()
    h.update(language.encode())
    h.update(b"\0")
    h.update(os.path.basename(voice_path).encode())
    h.update(b"\0")
    h.update(text.encode("utf-8"))
    return h.hexdigest()[:16]


def ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        sys.exit(
            "ffmpeg не найден в PATH. Установите:\n"
            "  Windows: winget install Gyan.FFmpeg\n"
            "  macOS:   brew install ffmpeg"
        )


def load_xtts(use_gpu: bool):
    """Импортируем тяжёлый TTS только когда реально нужен."""
    from TTS.api import TTS  # type: ignore

    print("Загружаю XTTS-v2 (~2 ГБ при первом запуске)...", file=sys.stderr)
    return TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=use_gpu)


def synthesize_chunk(tts, text: str, voice_path: str, language: str, out_wav: Path) -> None:
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    tts.tts_to_file(
        text=text,
        speaker_wav=voice_path,
        language=language,
        file_path=str(out_wav),
        split_sentences=False,
    )


def concat_wavs(wavs: list[Path], out_wav: Path, silence_ms: int = 250) -> None:
    """Склеиваем wav-чанки через ffmpeg concat-filter и вставляем короткие паузы."""
    if not wavs:
        raise ValueError("Нет аудиокусков для склейки.")
    listing = out_wav.parent / (out_wav.stem + ".list.txt")
    silence = out_wav.parent / (out_wav.stem + ".silence.wav")

    # Генерируем тишину один раз (24kHz mono, как у XTTS-v2).
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"anullsrc=r=24000:cl=mono",
            "-t", f"{silence_ms / 1000:.3f}",
            str(silence),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    lines: list[str] = []
    for w in wavs:
        lines.append(f"file '{w.as_posix()}'")
        lines.append(f"file '{silence.as_posix()}'")
    listing.write_text("\n".join(lines) + "\n", encoding="utf-8")

    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
         "-c", "copy", str(out_wav)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    listing.unlink(missing_ok=True)
    silence.unlink(missing_ok=True)


def encode_output(chapter_wavs: list[tuple[str, Path]], output: Path) -> None:
    """Финальное кодирование. .m4b — с разметкой глав, .mp3 — простая склейка."""
    suffix = output.suffix.lower()
    if suffix not in {".m4b", ".m4a", ".mp3"}:
        sys.exit(f"Неподдерживаемый формат вывода: {suffix} (нужно .m4b или .mp3)")

    if suffix in {".m4b", ".m4a"}:
        # Метаданные глав в формате ffmetadata1.
        meta_path = output.with_suffix(output.suffix + ".meta")
        cursor_ms = 0
        meta_lines = [";FFMETADATA1"]
        list_path = output.with_suffix(output.suffix + ".list")
        list_lines: list[str] = []
        for title, wav in chapter_wavs:
            duration_ms = int(float(_probe_duration(wav)) * 1000)
            meta_lines.append("[CHAPTER]")
            meta_lines.append("TIMEBASE=1/1000")
            meta_lines.append(f"START={cursor_ms}")
            meta_lines.append(f"END={cursor_ms + duration_ms}")
            meta_lines.append(f"title={title}")
            cursor_ms += duration_ms
            list_lines.append(f"file '{wav.as_posix()}'")
        meta_path.write_text("\n".join(meta_lines) + "\n", encoding="utf-8")
        list_path.write_text("\n".join(list_lines) + "\n", encoding="utf-8")

        subprocess.run(
            ["ffmpeg", "-y",
             "-f", "concat", "-safe", "0", "-i", str(list_path),
             "-i", str(meta_path),
             "-map_metadata", "1",
             "-c:a", "aac", "-b:a", "96k",
             str(output)],
            check=True,
        )
        list_path.unlink(missing_ok=True)
        meta_path.unlink(missing_ok=True)
    else:
        list_path = output.with_suffix(output.suffix + ".list")
        list_path.write_text(
            "\n".join(f"file '{w.as_posix()}'" for _, w in chapter_wavs) + "\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["ffmpeg", "-y",
             "-f", "concat", "-safe", "0", "-i", str(list_path),
             "-c:a", "libmp3lame", "-b:a", "96k",
             str(output)],
            check=True,
        )
        list_path.unlink(missing_ok=True)


def _probe_duration(path: Path) -> str:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        text=True,
    )
    return out.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Озвучка книги через XTTS-v2 с клонированием голоса.")
    parser.add_argument("--input", required=True, type=Path, help="Путь к .txt (UTF-8).")
    parser.add_argument("--output", required=True, type=Path, help="Путь к .m4b или .mp3.")
    parser.add_argument("--voice", required=True, type=Path, help="Референсный .wav 6-30 секунд, моно, 24 кГц.")
    parser.add_argument("--language", default="ru", help="Код языка для XTTS (ru, en, ...).")
    parser.add_argument("--accent", action="store_true", help="Расставлять ударения через ruaccent (нужен русский).")
    parser.add_argument("--no-gpu", action="store_true", help="Принудительно CPU (медленно, но работает везде).")
    parser.add_argument("--chunk-chars", type=int, default=240, help="Целевая длина чанка в символах.")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Не найден входной файл: {args.input}", file=sys.stderr)
        return 1
    if not args.voice.exists():
        print(f"Не найден сэмпл голоса: {args.voice}", file=sys.stderr)
        return 1

    ensure_ffmpeg()

    raw = args.input.read_text(encoding="utf-8")
    chapters = split_chapters(raw)
    print(f"Глав: {len(chapters)}")

    cache_dir = args.output.with_suffix(args.output.suffix + ".cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    index_path = cache_dir / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8")) if index_path.exists() else {}

    tts = load_xtts(use_gpu=not args.no_gpu)

    chapter_wavs: list[tuple[str, Path]] = []
    total_chunks = 0
    plan: list[tuple[int, str, list[str]]] = []
    for idx, ch in enumerate(chapters):
        norm = normalize(ch.text, accent=args.accent)
        sentences = split_sentences(norm)
        chunks = pack_chunks(sentences, max_chars=args.chunk_chars)
        plan.append((idx, ch.title, chunks))
        total_chunks += len(chunks)
    print(f"Всего чанков: {total_chunks}")

    with tqdm(total=total_chunks, unit="chunk", desc="Озвучка") as bar:
        for idx, title, chunks in plan:
            ch_wavs: list[Path] = []
            for chunk_text in chunks:
                key = sentence_hash(chunk_text, str(args.voice), args.language)
                wav = cache_dir / f"{key}.wav"
                if not wav.exists():
                    synthesize_chunk(tts, chunk_text, str(args.voice), args.language, wav)
                    index[key] = chunk_text[:80]
                    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
                ch_wavs.append(wav)
                bar.update(1)

            chapter_out = cache_dir / f"chapter_{idx:04d}.wav"
            concat_wavs(ch_wavs, chapter_out)
            chapter_wavs.append((title, chapter_out))

    print("Кодирую финальный файл...", file=sys.stderr)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    encode_output(chapter_wavs, args.output)
    print(f"Готово: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
