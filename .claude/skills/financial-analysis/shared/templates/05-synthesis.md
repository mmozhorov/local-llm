# Synthesis — <TICKER> от <YYYY-MM-DD>

## Сценарии

### Bull

- **Предпосылки (3-5):** <…>
- **Драйверы:** <…>
- **Target:** $<…>
- **P:** <%>
- **Leading indicator подтверждения:** <…>
- **Leading indicator опровержения:** <…>

### Base

- **Предпосылки:** <…>
- **Драйверы:** <…>
- **Target:** $<…>
- **P:** <%>
- **Leading indicator подтверждения:** <…>
- **Leading indicator опровержения:** <…>

### Bear

- **Предпосылки:** <…>
- **Драйверы:** <…>
- **Target:** $<…>
- **P:** <%>
- **Leading indicator подтверждения:** <…>
- **Leading indicator опровержения:** <…>

**Σ P = 100%**. **E(price) = Σ P_i × Target_i = $<…>**

## Сравнение с текущей ценой

| Параметр | Значение |
| Текущая цена | $<…> на <дата> |
| E(price) | $<…> |
| Апсайд / даунсайд | <%> |

## Sensitivity table (key drivers)

|             | g = 1% | g = 2% | g = 3% |
| margin 25%  |   |   |   |
| margin 28%  |   |   |   |
| margin 31%  |   |   |   |

(Выбери 2 самых чувствительных параметра из фазы 2.)

## Risk register

| Риск | P | Impact | Митигация | Kill switch |
| ... | ... | ... | ... | <конкретное условие выхода> |
| ... |  |  |  |  |

## Cross-check

- [ ] Σ вероятностей сценариев = 100%
- [ ] Bull / Bear покрывают экстремумы, не «два base»
- [ ] Каждый сценарий имеет leading indicators ↑ и ↓
- [ ] Risk register имеет конкретные kill switches (не «если плохо»)
- [ ] Технический setup (фаза 3) согласован с base case
- [ ] Триггеры из фазы 4 учтены как leading indicators
