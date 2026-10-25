#!/usr/bin/python3
"""Source-only FORMAT1 entry. No target import; exact Root READY required."""
import hashlib
import importlib.machinery
import os
import pathlib
import stat
import sys
import types

GUARD = pathlib.Path('/tmp/qcl-docs-routing-pure-guard-v4.py')
GUARD_SHA = 'c6534b6f1cf129877cd80482ebaddce7664dc179ff7f03760acef37f0f7a820c'

def entry():
    info = GUARD.lstat()
    if GUARD.resolve(strict=True) != GUARD or not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_size>131072:
        raise RuntimeError('reviewed source guard owner/type/size')
    with GUARD.open('rb') as stream:
        payload = stream.read(131073)
    if len(payload)!=info.st_size or hashlib.sha256(payload).hexdigest()!=GUARD_SHA:
        raise RuntimeError('reviewed source guard exact buffer')
    module = types.ModuleType('reviewed_pure_source_guard_FORMAT1')
    module.__file__,module.__package__,module.__loader__,module.__cached__ = str(GUARD),'',None,None
    module.__spec__ = importlib.machinery.ModuleSpec(module.__name__,loader=None,origin=str(GUARD))
    module.__spec__.has_location = True
    exec(compile(payload,str(GUARD),'exec',dont_inherit=True,optimize=0),module.__dict__)
    own = pathlib.Path(__file__)
    return module.source_main('FORMAT1',own,module.read_file(own),payload)

if __name__ == '__main__':
    sys.exit(entry())
