"""Check the old/fresh retarded residual and exact FDT contents of an aligned checkpoint."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib

import numpy as np

ROOT=Path(__file__).resolve().parent
RUN=ROOT/"attempt01"
CHANNELS=("LO","acoustic","impurity","IFR","alloy","embedding","embedding_plus","embedding_minus")


def sha(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()


def verify(checkpoint):
    terminal=tomllib.loads(checkpoint.with_name(checkpoint.name+".toml").read_text())
    assert sha(checkpoint)==terminal["sha256"]
    with tempfile.TemporaryDirectory(prefix="fath-proj-audit-") as temp:
        datafile=Path(temp)/"field.bin"
        def read(file,key,shape,dtype="<f8"):
            subprocess.run(["h5dump","-b","LE","-o",datafile,"-d","/"+key,file],
                           check=True,stdout=subprocess.DEVNULL)
            x=np.fromfile(datafile,dtype=dtype).reshape(shape)
            assert np.isfinite(x).all()
            return x
        def z(key):
            shape=(7,7,4,1201)
            return read(checkpoint,key+"_real",shape)+1j*read(checkpoint,key+"_imag",shape)
        assert read(checkpoint,"map",(),"<i8").item()==terminal["maps"]
        assert np.all(read(checkpoint,"hartree",(144,))==0)
        g, a, gl, gg=[z("green/"+n) for n in ("GR","A","GL","GG")]
        model=RUN/"model.h5"
        energy=read(model,"energy_dimensionless",(1201,))*.1
        we,wk=read(model,"weight_energy",(1201,)),read(model,"weight_k",(4,))
        rrs={}
        sum_old=np.zeros_like(g)
        sum_new=np.zeros_like(g)
        for name in CHANNELS:
            old=z("accepted_R/"+name)
            new=z("fresh/"+name+"/R")
            rrs[name]=np.linalg.norm(new-old)/(np.linalg.norm(new)+1e-14)
            if name not in ("embedding_plus","embedding_minus"):
                sum_old+=old
                sum_new+=new
        rtotal=np.linalg.norm(sum_new-sum_old)/(np.linalg.norm(sum_new)+1e-14)
    x=(energy-terminal["mu_meV"]/1000)/(10*1.380649e-23/1.602176634e-19)
    u=np.exp(-abs(x))
    f=np.where(x>=0,u/(1+u),1/(1+u))
    h=np.where(x>=0,1/(1+u),u/(1+u))
    diff=lambda x,y: float(np.linalg.norm(x-y)/(np.linalg.norm(y)+1e-14))
    rho=np.trace(-1j*gl,axis1=0,axis2=1).real
    density=np.sum(wk[:,None]*we[None,:]*rho)/np.pi
    result={
        "file":checkpoint.name,"map":terminal["maps"],"sha256":terminal["sha256"],
        "rR_max_family":float(max(rrs.values())),"rR_total":float(rtotal),
        "rR_max_abs_difference":abs(max(rrs.values())-terminal["rR_max_family"]),
        "rR_total_abs_difference":abs(rtotal-terminal["rR_total"]),
        "A_from_GR_relative":diff(a,1j*(g-g.swapaxes(0,1).conj())),
        "Gless_FDT_relative":diff(gl,1j*f*a),"Ggreater_FDT_relative":diff(gg,-1j*h*a),
        "number_relative_to_target_error":abs(density/.03-1),
    }
    assert max(result[k] for k in ("rR_max_abs_difference","rR_total_abs_difference",
        "A_from_GR_relative","Gless_FDT_relative","Ggreater_FDT_relative",
        "number_relative_to_target_error"))<1e-11
    return result


if __name__=="__main__":
    assert len(sys.argv)>1
    for name in sys.argv[1:]:
        file=RUN/name
        proof=verify(file)
        (ROOT/("audit-"+file.stem+".json")).write_text(json.dumps(proof,indent=2)+"\n")
        print(proof)
