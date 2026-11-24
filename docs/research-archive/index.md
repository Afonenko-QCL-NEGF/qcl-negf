# Исследовательский архив QCL NEGF

Библиотека связывает опубликованные исследования, рабочие точки, первичные численные свидетельства и научные выводы. В карточках видны прямые и обратные связи. Отчёты и численные данные сохраняют свои исходные адреса.

```{toctree}
:maxdepth: 2

queries
inventory
historical
benchmarks
fath-early
v843
fath54-night
fath54-local
fath54-k31-rank
fath54-common-q
vocabulary
methods
literature
```

## Сборка

Из корня приложения с установленными Python и Graphviz (`dot`):

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r docs/research-archive/requirements.txt
sphinx-build -n -W -b html docs/research-archive build/research-archive
```

Откройте `build/research-archive/index.html`. В этой же папке экспортируется
`needs.json`, сформированный Sphinx-Needs. В GitHub Actions откройте
[Research archive](https://github.com/Afonenko-QCL-NEGF/qcl-negf/actions/workflows/research-archive.yml)
и скачайте архив `research-archive-html` успешной сборки нужной ревизии.

Исходные отчёты доступны в [каталоге исследований](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/README.md).
