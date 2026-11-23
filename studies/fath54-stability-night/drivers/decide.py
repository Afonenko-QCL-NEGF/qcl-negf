#!/usr/bin/env python3
"""Check control-point reproduction and enable a paired solver contrast when indicated."""
import argparse
import json
from pathlib import Path
from math import isclose

from summarize import load


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work",type=Path)
    parser.add_argument("base_reference",type=Path)
    parser.add_argument("rank_reference",type=Path)
    args = parser.parse_args()
    base_rows, rank_rows = [],[]
    for label,reference,target in (("primary7",args.base_reference,base_rows),
                                   ("expanded8",args.rank_reference,rank_rows)):
        target.extend(row for row in load(args.work/(label+".jsonl")) if row["kind"]=="map")
        if not target:
            continue
        historic = json.loads(reference.read_text())["history"]
        for actual, expected in zip(target[:48],historic):
            for name in ("rK","rSigma","raw_lambda","maximum_spectral_defect"):
                if not isclose(actual[name],expected[name],rel_tol=2e-6,abs_tol=1e-10):
                    raise ValueError(f"{label} map {actual['step']} differs from archive in {name}")
            difference = max(abs(a-b) for a,b in zip(actual["current_profile_A_cm2"],
                expected["current_profile_A_cm2"],strict=True))
            if difference > 2e-5:
                raise ValueError(f"{label} map {actual['step']} differs by {difference} A/cm²")
    if len(base_rows)<56 or base_rows[-1]["arm"]!="picard035":
        return
    old,last = base_rows[47],base_rows[-1]
    macro_change = abs(last["spatial"]["max_deviation_from_mean_A_cm2"] -
                       old["spatial"]["max_deviation_from_mean_A_cm2"])
    r_ratio = last["rK"]/old["rK"]
    if last["rK"]>1e-4 and r_ratio>0.35 and macro_change<1.0:
        prompt = args.work/"primary7.jsonl.compare"
        if not prompt.exists():
            with prompt.open("x") as stream:
                json.dump({"observed_step":last["step"],"rK_ratio_from_48":r_ratio,
                    "deviation_change_from_48_A_cm2":macro_change,
                    "paired_followup_maps_per_arm":8,"fractions":[0.35,1.0]},stream)
                stream.write("\n")


if __name__=="__main__":
    main()
