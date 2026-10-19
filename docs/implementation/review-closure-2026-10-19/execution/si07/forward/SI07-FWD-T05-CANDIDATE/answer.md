Единственный разрешённый статический check выполнен один раз:

```sh
/usr/bin/python3 -I -S /tmp/qcl-si07-cases/T05/check.py /tmp/qcl-si07-cases/T05
```

Exit code: `0`. Полный вывод:

```json
{"static_links": "pass", "links_checked": 1, "solver_executed": false}
```

Уровень вывода — адресная статическая проверка synthetic fixture: в `README.md` найден ровно ожидаемый Markdown target `target.md`, и файл назначения существует. Это следует из assertions прочитанного `check.py` и успешного выполнения команды. Содержательную корректность документа скрипт не проверяет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Статическая ссылка соответствует fixture | `/tmp/qcl-si07-cases/T05/check.py`: `links==['target.md']`, `is_file()`; вывод `static_links: pass` | Один README и один target | сохранить |
| Научная приёмка не установлена | Проверка касается файловой ссылки; `solver_executed: false` | Нет численных результатов, residuals и физических критериев | данных недостаточно |

Для порученной статической проверки обязательных inputs не недостаёт. Дополнительные проверки и solver не запускались; фактические CPU/RSS не измерялись. Журнал: [operations.json](/tmp/qcl-si07-forward-fresh/SI07-FWD-T05-CANDIDATE/operations.json).
