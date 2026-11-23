project = "Исследовательский архив QCL NEGF"
language = "ru"
myst_heading_anchors = 3
extensions = ["myst_parser", "sphinx.ext.graphviz", "sphinx_needs"]
myst_enable_extensions = ["dollarmath", "colon_fence"]
html_theme = "alabaster"
html_theme_options = {"page_width": "1100px"}
graphviz_output_format = "svg"
nitpicky = True
exclude_patterns = ["_build"]

needs_id_required = True
needs_id_regex = r"^Q(?:S|P|PAM|X|R|E|C|M|O|L)_[A-Z0-9_]+$"
needs_build_json = True
needs_flow_engine = "graphviz"

needs_types = [
    dict(directive=directive, title=title, prefix=prefix, color=color, style="rectangle")
    for directive, title, prefix, color in [
        ("qstructure", "Структура", "QS_", "#dce9f5"),
        ("qpoint", "Рабочая точка", "QP_", "#dce9f5"),
        ("qexperiment", "Сравнительный опыт", "QX_", "#dbefe5"),
        ("qrun", "Вариант или запуск", "QR_", "#dbefe5"),
        ("qevidence", "Свидетельство", "QE_", "#fff2cc"),
        ("qclaim", "Утверждение", "QC_", "#ffe2d6"),
        ("qparam", "Фактор", "QPAM_", "#e9e1f4"),
        ("qmechanism", "Механизм", "QM_", "#e9e1f4"),
        ("qobservable", "Наблюдаемая", "QO_", "#e9e1f4"),
        ("qsource", "Источник", "QL_", "#fff2cc"),
    ]
]

needs_fields = {
    name: {"description": description, "nullable": True}
    for name, description in {
        "family": "Семейство исследования",
        "bias_kind": "Вид смещения",
        "bias_value": "Величина смещения",
        "bias_unit": "Единица смещения",
        "sign": "Конвенция знака",
        "temperature": "Температура",
        "optical": "Оптический режим",
        "stage": "Стадия расчёта или наблюдения",
        "stationarity": "Статус проверки стационарности",
        "criteria": "Заданный критерий",
        "verdict": "Фактический результат",
        "availability": "Доступность источника",
        "locator": "Координата в источнике",
        "role": "Роль свидетельства или варианта",
        "lo_mode": "Фактическое включение LO",
    }.items()
}

needs_links = {
    name: {"outgoing": outgoing, "incoming": incoming, "target_types": targets}
    for name, outgoing, incoming, targets in [
        ("structure", "Структура", "Связанные записи", ["qstructure"]),
        ("at", "В рабочей точке", "Опыты и варианты в точке", ["qpoint"]),
        ("varies", "Изменяет", "Изменяется в опытах", ["qparam"]),
        ("targets", "Проверяет механизм", "Механизм проверяется в", ["qmechanism"]),
        ("observes", "Наблюдает", "Наблюдаемая измерена в", ["qobservable"]),
        ("baseline", "Базовый вариант", "База для", ["qrun"]),
        ("variants", "Варианты", "Вариант опыта", ["qrun"]),
        ("same_input", "Общий вход", "Тот же вход использован в", ["qrun", "qevidence"]),
        ("evidence", "Свидетельства", "Свидетельство для", ["qevidence"]),
        ("supports", "Поддерживает", "Поддержано", ["qclaim"]),
        ("limits", "Ограничивает", "Ограничено", ["qclaim"]),
        ("contradicts", "Противоречит", "Противоречие со стороны", ["qclaim"]),
        ("source", "Первоисточник", "Используется в", ["qsource", "qevidence"]),
        ("depends", "Вычислительная зависимость", "Используется при вычислении", []),
    ]
}
for link in needs_links.values():
    if not link["target_types"]:
        del link["target_types"]

extensions += ["sphinxcontrib.bibtex"]
bibtex_bibfiles = ["../../studies/historical/literature/catalog.bib"]
bibtex_default_style = "unsrt"
