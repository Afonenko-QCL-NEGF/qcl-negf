"""Save compact measurements for the independent review and research archive."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from assess_fath import assess


def records(path):
    with path.open() as handle:
        return [json.loads(line) for line in handle]


def sha(path):
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def unique(rows, kind):
    return next(row for row in reversed(rows) if row["kind"] == kind)


def make_report(out, fath, bosco, summary):
    selection = unique(fath, "fath_scheme_selection")
    criteria = unique(fath, "rank_block_complete")
    final_bosco = unique(bosco, "finished")
    last_bosco = unique(bosco, "map")["row"]
    mode_card = [r for r in fath if r["kind"] in ("ninth_mode", "ninth_mode_error")]
    lines = [
        "# Fath 54 мВ на общей Q и независимая точка Bosco",
        "",
        "Численный протокол для независимой проверки. Вывод проверяющего ожидается.",
        "",
        "По замечанию пользователя транспортный ранг отделён от координатной "
        "проекции. Локальные энергетические и радиальные пробы определяют выбор "
        "уточнения с опорой на вклад в пространственный ток.",
        "",
        "## Fath, 10 К",
        "",
        "| Ветвь | Карта | W | Q | rK | rΣ | λ | Jср, А/см² | "
        "Макс. отклонение | Левый шов | Правый шов | ΔJ на 33,85–39,64 нм |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in summary["latest_sections"]:
        a, b = item["seams"]
        lines.append(
            f"| {item['name']} | {item['step']} | {item['W']} | {item['Q']} | "
            f"{item['rK']:.7g} | {item['rSigma']:.7g} | {item['lambda']:.9g} | "
            f"{item['mean']:.6g} | {item['max_deviation']:.6g} | "
            f"{a:.6g} | {b:.6g} | {item['jump']:+.6g} |"
        )
    lines += ["", "### Разность центрированных профилей", ""]
    if summary["resolved_decrease"]:
        lines.append("На двух сопоставимых поздних отметках верхняя оценка D₈₉ ниже нижней оценки D₇₈.")
    else:
        lines.append("Зарегистрированный критерий ослабления D₈₉ на двух поздних отметках не выполнен.")
    lines.append("")
    for match in summary["contrasts"]:
        line = f"- Карты {match['steps']}, отношения rK и rΣ {match['rK_ratio']:.4g} и {match['rSigma_ratio']:.4g}."
        for contrast in match["contrasts"]:
            err = contrast["interval"]
            interval = (f" [{err[0]:.6g}, {err[1]:.6g}]" if err else " (интервал не установлен)")
            line += f" D = {contrast['centered']:.6g}{interval} А/см²."
        lines.append(line)
    lines += [
        "",
        f"Число последовательных строгих карт по ветвям {criteria['names']} составляет "
        f"{criteria['confirmations']}. Для выбранной ветви воспроизводимость по второй "
        f"истории отмечена в поле `strict` протокола ({selection['chosen']['strict']}).",
        "",
        "### Подписанный баланс на 33,85–39,64 нм",
        "",
        "| Ветвь | Стадия | ΔJ | Остаток | Проекция | LO | Акустика | Примеси | IFR | Сплав | Замыкание |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in summary["latest_sections"]:
        for phase in ("fresh", "lagged"):
            bal = item[f"{phase}_balance"]["late7"]
            terms = bal["collisions_A_cm2"]
            parts = (bal["delta_J_A_cm2"], bal["source_lag_A_cm2"], bal["projection_A_cm2"],
                     *(terms[k] for k in ("LO", "acoustic", "impurity", "IFR", "alloy")),
                     bal["closure_A_cm2"])
            lines.append(f"| {item['name']} | {phase} | " + " | ".join(f"{n:+.6g}" for n in parts) + " |")
    lines += [
        "",
        "Состав базиса, краевые веса W9, фазовые пробы, сеточные контрасты, "
        "изменения Q при фиксированном W и ответ второй истории сохранены в "
        "первичных строках. Унитарные проверки и альтернативные физические модели "
        "из предыдущего архива служат исходными ограничениями.",
        "",
        f"Кандидаты W9 представлены {len(mode_card)} зарегистрированными проверками. "
        "Наблюдаемые и основания выбора воспроизводятся по [траектории Fath]"
        "(fath-trajectory.jsonl) и [численному своду](fath-assessment.json).",
        "",
        "## Перенос Bosco, 200 К и 56 мВ",
        "",
        "Параметры переноса и ревизии записаны [до первой карты Bosco](selected-scheme.json). "
        "Геометрия, H, ядра, причинный якорь и затравки построены для Bosco.",
        "",
        f"Средний ток по независимой квадратуре {final_bosco['mean_A_cm2']:.6g} А/см², "
        f"остаток относительно 3603,55 А/см² равен {final_bosco['reference_difference_A_cm2']:+.6g} А/см². "
        f"Квадратурное расхождение {final_bosco['quadrature_error']:.6g} А/см². "
        "Полуширина авторской линии 9,26 А/см², привязка напряжения рассматривается отдельно "
        "по соседним вершинам 3568,19–3603,55 А/см². Оптический режим авторской кривой не установлен.",
        "",
        f"На карте {final_bosco['step']} rK = {last_bosco['rK']:.7g}, "
        f"rΣ = {last_bosco['rSigma']:.7g}, λ = {last_bosco['raw_lambda']:.9g}, "
        f"спектральный дефект {last_bosco['maximum_spectral_defect']:.7g}. "
        f"Строгий статус {final_bosco['strict']}. Контроль швов, пространственная неоднородность "
        "и поздний дрейф приведены в [своде Bosco](bosco-summary.json).",
        "",
        "Для [карты плотности](bosco-density.csv) сохранены разметка областей по рисунку "
        "и интегралы с вариациями единой координатной и энергетической привязки. "
        "Населённости уровней 4 и 5 требуют надёжного сопоставления волновых функций.",
        "",
        "## Независимая сверка",
        "",
        "Здесь будут записаны самостоятельный вывод проверяющего по первичным данным, "
        "сопоставление трактовок и итоговое решение по альтернативам.",
    ]
    (out / "report-draft.md").write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trajectory", type=Path)
    args = parser.parse_args()
    work = args.trajectory.parent
    out = work / "evidence"
    out.mkdir(exist_ok=True)
    fath = records(args.trajectory)
    bosco = records(work / "bosco" / "trajectory.jsonl")
    summary = assess(fath)
    write_json(out / "fath-assessment.json", summary)
    write_json(out / "bosco-summary.json", {
        "configuration": unique(bosco, "configuration"),
        "final": unique(bosco, "finished"),
        "direct_observation": unique(bosco, "independent"),
        "signed_balance": unique(bosco, "signed_balance"),
        "final_map": unique(bosco, "map"),
    })
    for name, source in (
        ("fath-trajectory.jsonl", args.trajectory),
        ("f13-replay.json", work / "replay.json"),
        ("selected-scheme.json", work / "selected-bosco-scheme.json"),
        ("bosco-trajectory.jsonl", work / "bosco" / "trajectory.jsonl"),
        ("bosco-config.yaml", work / "bosco" / "point.yaml"),
        ("bosco-density.csv", work / "bosco" / "density.csv"),
    ):
        shutil.copyfile(source, out / name)
    make_report(out, fath, bosco, summary)
    manifests = sorted(path for path in out.iterdir() if path.name != "SHA256SUMS")
    (out / "SHA256SUMS").write_text("".join(f"{sha(path)}  {path.name}\n" for path in manifests))


if __name__ == "__main__":
    main()
