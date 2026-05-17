---
name: financial-analysis
description: "Активируй этот скилл всегда, когда пользователь просит проанализировать компанию, оценить акцию, дать инвестиционную рекомендацию или сделать due diligence. Координирует семь фаз: scoping → context → fundamental → technical → sentiment → synthesis → verdict."
---

# Financial Analysis — корневой роутер

Маршрутизирует пользовательский запрос по семи фазам анализа компании. Сам анализ не выполняет — только определяет, какой sub-skill активировать.

<HARD-GATE>
Никаких финальных рекомендаций (Buy/Hold/Sell, target price, рейтинг) до прохождения всех семи фаз и сохранения их артефактов. Это правило действует для ЛЮБОЙ компании.
</HARD-GATE>

## Skill-first protocol

Перед любым действием проверь, какая фаза активна. Активная фаза определяется тем, какой артефакт в `docs/research/<TICKER>/<YYYY-MM-DD>/` ещё не создан или не подтверждён пользователем.

| # | Фаза | Skill | Артефакт |
|---|---|---|---|
| 0 | Scoping | `00-scoping/SKILL.md` | `00-scope.md` |
| 1 | Company context | `01-company-context/SKILL.md` | `01-context.md` |
| 2 | Fundamental | `02-fundamental/SKILL.md` | `02-fundamental.md` (+ `02-dcf.md`) |
| 3 | Technical | `03-technical/SKILL.md` | `03-technical.md` |
| 4 | Sentiment / macro | `04-sentiment-macro/SKILL.md` | `04-sentiment.md` |
| 5 | Synthesis | `05-synthesis/SKILL.md` | `05-synthesis.md` |
| 6 | Verdict | `06-verdict/SKILL.md` | `06-verdict.md` |

## Алгоритм роутера

1. **Определи тикер.** Если в запросе только название компании — запроси тикер
   и рынок одним вопросом (multiple-choice, если вариантов несколько).
2. **Найди или создай рабочую папку** `docs/research/<TICKER>/<YYYY-MM-DD>/`.
3. **Определи следующую невыполненную фазу.** Загрузи её SKILL.md и следуй ему.
4. **Между фазами** — короткий чекпоинт пользователю:
   «Фаза N завершена, артефакт <path>. Переходим к фазе N+1? (да / правки)».
5. **После фазы 6** — финальный self-review (см. `shared/self-review.md`),
   потом всё.

## Что НЕ делать

- Не пропускай фазы, даже если пользователь просит «быстрый ответ».
  Вместо этого предложи сокращённый формат (короткие секции, минимум 3 строки),
  но прогон по всем фазам обязателен.
- Не давай target price из головы. Только из артефакта фазы 2 (DCF + multiples).
- Не комбинируй фазы в одном сообщении. Одна фаза — одно сообщение / артефакт.

## Ссылки

- Полный методологический документ: `docs/financial-agent.md`
- Каталог источников данных: `shared/data-sources.md`
- Каталог анти-паттернов: `shared/anti-patterns.md`
- Self-review checklist: `shared/self-review.md`
