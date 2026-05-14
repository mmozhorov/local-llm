"""Нормализация русского текста перед подачей в XTTS-v2.

Делаем три вещи:
  1. Разворачиваем числа в слова (1812 -> «тысяча восемьсот двенадцать»).
  2. Разворачиваем самые частые аббревиатуры (т.е. -> «то есть» и т. п.).
  3. Приводим пунктуацию к виду, который XTTS лучше читает (тире = пауза).

Опционально (если установлен ruaccent) — расставляем ударения, чтобы
модель меньше путала «за́мок/замо́к» и подобное.
"""

from __future__ import annotations

import re
from functools import lru_cache

from num2words import num2words


_ABBREVIATIONS = {
    r"\bт\.?\s?е\.": "то есть",
    r"\bт\.?\s?к\.": "так как",
    r"\bт\.?\s?д\.": "так далее",
    r"\bт\.?\s?п\.": "тому подобное",
    r"\bт\.?\s?н\.": "так называемый",
    r"\bи\s+т\.?\s?д\.": "и так далее",
    r"\bи\s+т\.?\s?п\.": "и тому подобное",
    r"\bг\.": "год",
    r"\bгг\.": "годы",
    r"\bв\.": "век",
    r"\bвв\.": "века",
    r"\bстр\.": "страница",
    r"\bср\.": "сравните",
    r"\bнапр\.": "например",
    r"\bр\.": "рублей",
    r"\bкоп\.": "копеек",
    r"\bдр\.": "другие",
    r"\bпроф\.": "профессор",
    r"\bим\.": "имени",
    r"\bтыс\.": "тысяч",
    r"\bмлн\b": "миллионов",
    r"\bмлрд\b": "миллиардов",
}


@lru_cache(maxsize=2048)
def _num_to_ru(n: int) -> str:
    return num2words(n, lang="ru")


def _replace_numbers(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        digits = match.group(0)
        try:
            return _num_to_ru(int(digits))
        except (ValueError, OverflowError):
            return digits

    return re.sub(r"\b\d{1,9}\b", repl, text)


def _expand_abbreviations(text: str) -> str:
    for pattern, replacement in _ABBREVIATIONS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def _normalize_punctuation(text: str) -> str:
    text = text.replace("—", ",").replace("–", ",")  # em / en dash → запятая-пауза
    text = text.replace("«", "").replace("»", "")  # «» убираем, на интонацию не влияют
    text = text.replace("“", "").replace("”", "")  # английские кавычки
    text = re.sub(r"\.{3,}", "…", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize(text: str, accent: bool = False) -> str:
    """Полная цепочка нормализации.

    Если `accent=True` и установлен ruaccent — расставляет ударения.
    """
    text = _expand_abbreviations(text)
    text = _replace_numbers(text)
    text = _normalize_punctuation(text)
    if accent:
        try:
            from ruaccent import RUAccent  # type: ignore
        except ImportError:
            return text
        accentizer = _get_accentizer()
        text = accentizer.process_all(text)
    return text


@lru_cache(maxsize=1)
def _get_accentizer():
    from ruaccent import RUAccent  # type: ignore

    a = RUAccent()
    a.load(omograph_model_size="turbo", use_dictionary=True)
    return a


_SENT_END = re.compile(r"(?<=[.!?…])\s+(?=[А-ЯA-Z«\"„])")


def split_sentences(text: str) -> list[str]:
    """Простое разбиение по концу предложения. Хватает для прозы; для научного текста с
    сокращениями лучше брать spacy/razdel, но это тянет лишние зависимости."""
    parts = _SENT_END.split(text)
    return [p.strip() for p in parts if p.strip()]


def pack_chunks(sentences: list[str], max_chars: int = 240) -> list[str]:
    """XTTS-v2 теряет качество на кусках длиннее ~250 символов и режет фразу
    в неудачных местах. Поэтому собираем буфер из коротких предложений и
    отправляем длинные по одному."""
    chunks: list[str] = []
    buf: list[str] = []
    buf_len = 0
    for s in sentences:
        if len(s) >= max_chars:
            if buf:
                chunks.append(" ".join(buf))
                buf, buf_len = [], 0
            chunks.append(s)
            continue
        add_len = len(s) + (1 if buf else 0)
        if buf_len + add_len > max_chars:
            chunks.append(" ".join(buf))
            buf = [s]
            buf_len = len(s)
        else:
            buf.append(s)
            buf_len += add_len
    if buf:
        chunks.append(" ".join(buf))
    return chunks
