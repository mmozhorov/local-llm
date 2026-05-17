# Каталог источников данных

Что использовать в зависимости от фазы и доступа.

## Бесплатные / public

| Источник | Для чего | Покрытие |
|---|---|---|
| SEC EDGAR (`sec.gov/edgar`) | 10-K, 10-Q, 8-K, 13F, S-1 | США |
| e-disclosure.ru | Годовая, ежеквартальная отчётность | Россия |
| Yahoo Finance / `yfinance` (Python) | Цены, дивиденды, базовые financials, peers | Global |
| TradingView | Графики, индикаторы, screener | Global |
| Finviz | Скрининг, базовая TA, news headlines | US |
| FRED (St. Louis Fed) | Макро: ставки, CPI, безработица | US + global |
| Damodaran data (`pages.stern.nyu.edu/~adamodar`) | β по отраслям, ERP по странам, отраслевые мультипликаторы | Global |
| Company IR site | Годовые/квартальные отчёты, гайденс, презентации, транскрипты | Конкретная компания |
| MOEX ISS API | Цены, корп. события, индексы | Россия |

## Платные / freemium

| Источник | Что даёт | Когда нужен |
|---|---|---|
| Bloomberg Terminal | Институциональный стандарт | Sell-side / buy-side professional |
| Refinitiv Eikon | Аналог Bloomberg | Аналогично |
| Koyfin | Дешёвый Bloomberg для retail | Серьёзная самостоятельная работа |
| Tikr.com | Clean financials, screener | Quick valuation |
| Stockanalysis.com | Финансовая отчётность в удобной форме | Quick lookup |
| Sentieo / AlphaSense | Поиск по транскриптам и SEC | Глубокое qualitative |
| Financial Modeling Prep API | Programmatic financials | Скрипты |

## API для агента (Python)

| Пакет | Для чего |
|---|---|
| `yfinance` | Цены, дивиденды, базовые мультипликаторы, OHLCV |
| `pandas-ta` или `TA-Lib` | Локальный расчёт индикаторов TA |
| `requests` / `httpx` | Любые REST API |
| `apimoex` | MOEX данные для России |
| `fredapi` | Макро от FRED |
| `gnews` / NewsAPI | Свежие новости |

## Правило свежести

- **Цены / OHLCV** — не старше end-of-day предыдущей сессии.
- **Финансовая отчётность** — последний доступный квартал; если прошло > 90 дней
  после конца квартала и нет нового отчёта — флаг.
- **Новости** — окно 30–60 дней для sentiment-фазы, окно 12 месяцев для context.
- **Sell-side targets** — окно 90 дней.

## Web search

Для фаз 1 (context) и 4 (sentiment / macro) **web search обязателен** — без него LLM
с высокой вероятностью подсунет устаревшие или вымышленные данные.

- В Claude Code — WebSearch / WebFetch / Exa MCP.
- В локальном Ollama — web search недоступен из коробки; работаем в режиме
  «human as web»: пользователь приносит свежие материалы (отчёт, статьи).
  Все выводы помечаются `cutoff: <model_knowledge_date>`.
