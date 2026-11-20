"""Apply the independent archive checks to the continuation's original-stock state."""
import importlib.util
import json
from pathlib import Path

here=Path(__file__).resolve().parent
origin=here.parent/"independent.py"
spec=importlib.util.spec_from_file_location("fath_stock_independent",origin)
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
audit.RUN=here/"attempt01"
audit.MODEL=audit.RUN/"model.h5"
audit.STATE=audit.RUN/"state.h5"
(here/"independent.json").write_text(json.dumps(audit.check(),indent=2)+"\n")
