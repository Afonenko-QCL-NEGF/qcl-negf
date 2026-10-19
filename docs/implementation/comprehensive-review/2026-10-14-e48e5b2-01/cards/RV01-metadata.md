# RV01 metadata: контракт

Вопрос: какие поля наблюдавшегося S01 подтверждаются saved originals?
Owner Results/Research, writer coordinator, reviewer pending.
Denominator: source/installed/imported; receipt 5 JSON pointers; plan/schema/model/fingerprints; run/CalcJob/attempt; part/raw completeness; 5 evidence levels.
Входы: source-receipt.json, frozen source audit; exact bounded originals из RV01.md.
Разрешённые записи RV01.md, fixes/RV01-*.md. Oracle — SHA256 original+exact JSON selection; negative technical completed/scientific false, stale RUNNING, missing final HDF5.
Проверка: metadata Python stdlib, до 256KiB I/O, no archive extraction/arrays/SSH.
Budget: writer 6мин + reviewer <=8мин, <=1CPU <=1GiB; extracts <=96KiB, report <=8KiB.
Stop: все поля disposition либо missing; numeric claims запрещены.
