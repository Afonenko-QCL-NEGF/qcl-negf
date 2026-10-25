#!/usr/bin/python3
"""Source-only CHECK4 diagnostic entry; requires high review and fresh Root READY."""
import hashlib
import importlib.machinery
import os
import pathlib
import stat
import sys
import types

GUARD = pathlib.Path('/tmp/qcl-docs-routing-pure-guard-v9.py')
GUARD_SHA = 'e02576c6b421b158a00a570ca729b076737d47c1e79111606d15fb60a2cba01e'

def entry():
    info = GUARD.lstat()
    if GUARD.resolve(strict=True) != GUARD or not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_size>131072:
        raise RuntimeError('reviewed source guard owner/type/size')
    with GUARD.open('rb') as stream:
        payload = stream.read(131073)
    if len(payload)!=info.st_size or hashlib.sha256(payload).hexdigest()!=GUARD_SHA:
        raise RuntimeError('reviewed source guard exact buffer')
    module = types.ModuleType('reviewed_pure_source_guard_CHECK4')
    module.__file__,module.__package__,module.__loader__,module.__cached__ = str(GUARD),'',None,None
    module.__spec__ = importlib.machinery.ModuleSpec(module.__name__,loader=None,origin=str(GUARD))
    module.__spec__.has_location = True
    exec(compile(payload,str(GUARD),'exec',dont_inherit=True,optimize=0),module.__dict__)
    own = pathlib.Path(__file__)
    return module.source_main('CHECK4',own,module.read_file(own),payload)

if __name__ == '__main__':
    sys.exit(entry())
