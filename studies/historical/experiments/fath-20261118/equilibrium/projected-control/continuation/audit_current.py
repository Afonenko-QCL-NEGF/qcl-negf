"""Independent current-gate and cancellation audit of the final zero-field stock."""
import csv
import hashlib
import json
from math import fsum
from pathlib import Path
import statistics
import subprocess
import tempfile
import tomllib

import numpy as np

HERE=Path(__file__).resolve().parent
RUN=HERE/"attempt01"
ZERO=HERE.parents[1]/"attempt01/linear"
FLOOR=1e-16    # 1e-12 A/m^2 after conversion to A/cm^2
R_OBS=1e-4


def sha(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()


def history():
    with (RUN/"stock.csv").open() as f:
        rows=list(csv.DictReader(f))
    results=[]
    for index,r in enumerate(rows):
        plus,minus=float(r["Jplus_A_cm2"]),float(r["Jminus_A_cm2"])
        old=None if index==0 else float(rows[index-1]["Jplus_A_cm2"])
        delta=None if old is None else abs(plus-old)
        scale=None if old is None else max(abs(plus),abs(old),FLOOR)
        relative=None if scale is None else delta/scale
        if index:
            assert abs(relative-float(r["rJchange"]))<1e-12
        results.append({
            "stock_map":int(r["stock_map"]),"Jplus_A_cm2":plus,"Jminus_A_cm2":minus,
            "Jnet_A_cm2":plus+minus,"delta_abs_Jplus_A_cm2":delta,"denominator_A_cm2":scale,
            "allowed_delta_Jplus_A_cm2":None if scale is None else R_OBS*scale,
            "independent_rJchange":relative,"native_rJchange":float(r["rJchange"]),
            "floor_active":False if scale is None else scale==FLOOR,"strict":r["strict"],
            "failed":r["failed"],
        })
    with (HERE/"current_gate.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)

    old=[]
    for n in range(240,257):
        rec=tomllib.loads((ZERO/"rows"/f"{n:03d}.toml").read_text())
        old.append(rec["J"]/1e4)
    new=results[-16:]
    def mean_abs(values): return statistics.mean(map(abs,values))
    return {
        "maps":len(rows), "delta_floor_A_cm2":FLOOR, "relative_gate":R_OBS,
        "floor_active_nontechnical_rows":sum(r["floor_active"] for r in results),
        "min_relative_with_predecessor":min(r["independent_rJchange"] for r in results[1:]),
        "cold_last16_mean_signed_Jplus_A_cm2":statistics.mean(old[1:]),
        "cold_last16_mean_abs_Jplus_A_cm2":mean_abs(old[1:]),
        "cold_last16_mean_abs_delta_Jplus_A_cm2":statistics.mean(abs(b-a) for a,b in zip(old[:-1],old[1:])),
        "stock_last16_mean_signed_Jplus_A_cm2":statistics.mean(r["Jplus_A_cm2"] for r in new),
        "stock_last16_mean_abs_Jplus_A_cm2":mean_abs(r["Jplus_A_cm2"] for r in new),
        "stock_last16_mean_abs_Jminus_A_cm2":mean_abs(r["Jminus_A_cm2"] for r in new),
        "stock_last16_mean_abs_delta_Jplus_A_cm2":statistics.mean(r["delta_abs_Jplus_A_cm2"] for r in new),
        "failed_only_J_rows":sum(r["failed"]=="r_Jchange" for r in results),
        "joint_strict_pass_rows":sum(r["strict"]=="true" for r in results),
        "spectral_sum_min_max":[min(float(r["r_sum"]) for r in rows),max(float(r["r_sum"]) for r in rows)],
    }


def gross(μ):
    state,model=RUN/"state.h5",RUN/"model.h5"
    summary=tomllib.loads((RUN/"summary.toml").read_text())
    assert sha(state)==summary["state_sha256"] and sha(model)==summary["model_sha256"]
    with tempfile.TemporaryDirectory(prefix="fath-current-audit-") as temp:
        data=Path(temp)/"field.bin"
        def read(file,name,shape):
            subprocess.run(["h5dump","-b","LE","-o",data,"-d","/"+name,file],
                           check=True,stdout=subprocess.DEVNULL)
            return np.fromfile(data,dtype="<f8").reshape(shape).astype(np.longdouble)
        def field(name):
            shape=(7,7,4,1201)
            value=read(state,name+"_real",shape)+1j*read(state,name+"_imag",shape)
            return np.ascontiguousarray(value.transpose(3,2,1,0),dtype=np.clongdouble)
        e=read(model,"energy_dimensionless",(1201,))*.1
        we,wk=read(model,"weight_energy",(1201,)),read(model,"weight_k",(4,))
        weights=we[:,None]*wk[None,:]
        gn,gp=-1j*field("green/GL"),1j*field("green/GG")
        gtotal=gn+gp
        kbT=np.longdouble(10)*np.longdouble("1.380649e-23")/np.longdouble("1.602176634e-19")
        q=np.exp(-np.abs((e-μ)/kbT))
        f=np.where(e>=μ,q/(1+q),1/(1+q))[:,None,None,None]
        residual_g=gn-f*gtotal
        electron=np.longdouble("1.602176634e-19")
        hbar=np.longdouble("1.054571817e-34")
        # g_s=2, E0=.1 eV and L0=10 nm. Units here A/cm^2.
        factor=electron**2*np.longdouble(".1")/(hbar*np.longdouble("1e-16"))/np.longdouble(1e4)/np.arccos(np.longdouble(-1))
        ans={}
        tr=lambda a,b: np.einsum("...ij,...ji->...",a,b).real
        net=lambda q: float(factor)*fsum((weights*q).ravel())
        for side in ("plus","minus"):
            prefix="selfenergy/embedding_"+side
            sn,sp=-1j*field(prefix+"/L"),1j*field(prefix+"/G")
            out,inc=tr(sp,gn),tr(sn,gp)
            separation=out-inc
            gamma=sn+sp
            first=net(tr(gamma,residual_g))
            second=-net(tr(sn-f*gamma,gtotal))
            Jout,Jin=net(out),net(inc)
            net_fsum=net(separation)
            native=history_latest("J"+side+"_A_cm2")
            ans[side]=dict(gross_out_A_cm2=Jout,gross_in_A_cm2=Jin,net_fsum_A_cm2=net_fsum,
                net_plain_longdouble_A_cm2=float(factor*np.sum(weights*separation,dtype=np.longdouble)),
                component_green_deviation_A_cm2=first,component_contact_deviation_A_cm2=second,
                compensated_identity_abs_error_A_cm2=abs(first+second-net_fsum),
                native_minus_compensated_A_cm2=native-net_fsum,
                cancellation_ratio=abs(net_fsum)/(abs(Jout)+abs(Jin)))
    return ans


def history_latest(key):
    with (RUN/"stock.csv").open() as tr:
        return float(list(csv.DictReader(tr))[-1][key])


def main():
    independent=json.loads((HERE/"independent.json").read_text())
    data=history()
    data["terminal_compensated_currents"]=gross(independent["FDT_mu_meV"]/1000)
    (HERE/"current_gate.json").write_text(json.dumps(data,indent=2)+"\n")


if __name__=="__main__":
    main()
