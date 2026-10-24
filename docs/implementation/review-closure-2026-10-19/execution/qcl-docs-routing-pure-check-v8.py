#!/usr/bin/python3
"""Source-only CHECK3 entry; compiler no cached-only; requires Root READY."""
import hashlib
import importlib.machinery
import os
import pathlib
import stat
import sys
import types

GUARD = pathlib.Path('/tmp/qcl-docs-routing-pure-guard-v8.py')
GUARD_SHA = '5cecec92f20bed186ab51b08b4b98585dde5452af5e4eef31ad27adbf386763b'

def entry():
    info = GUARD.lstat()
    if GUARD.resolve(strict=True) != GUARD or not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_size>131072:
        raise RuntimeError('reviewed source guard owner/type/size')
    with GUARD.open('rb') as stream:
        payload = stream.read(131073)
    if len(payload)!=info.st_size or hashlib.sha256(payload).hexdigest()!=GUARD_SHA:
        raise RuntimeError('reviewed source guard exact buffer')
    module = types.ModuleType('reviewed_pure_source_guard_CHECK3')
    module.__file__,module.__package__,module.__loader__,module.__cached__ = str(GUARD),'',None,None
    module.__spec__ = importlib.machinery.ModuleSpec(module.__name__,loader=None,origin=str(GUARD))
    module.__spec__.has_location = True
    exec(compile(payload,str(GUARD),'exec',dont_inherit=True,optimize=0),module.__dict__)
    own = pathlib.Path(__file__)
    return module.source_main('CHECK3',own,module.read_file(own),payload)

if __name__ == '__main__':
    sys.exit(entry())
