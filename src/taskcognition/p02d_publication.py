"""P02D v3 file protocol: durable bytes, then atomic no-clobber publication.

Same-directory hard-link creation on the workstation filesystem is the commit.
The .pending name is never a reader/ledger name. No overwrite fallback exists.
fsync prepares file contents; this is not a power-loss guarantee for directories.
Single supervisor owns ledger ordering. Concurrent readers see committed prefixes.
"""
import os
import tempfile
from pathlib import Path
from .artifacts import read_json
from .contracts import canonical, IntegrityError

def _prepare(path, value):
    data=canonical(value)+b'\n'  # serialization failure cannot expose a final path
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.'+path.name+'.',suffix='.pending',dir=path.parent)
    temporary=Path(name)
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(data);stream.flush();os.fsync(stream.fileno())
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    return temporary

def write_new(path,value):
    path=Path(path);temporary=_prepare(path,value)
    try:
        os.link(temporary,path)  # atomic create, fails if destination already exists
    finally:
        temporary.unlink(missing_ok=True)

def replace_state(path,value):
    """Only mutable phase state uses replacement; never immutable evidence/IPC."""
    temporary=_prepare(path,value)
    try:os.replace(temporary,path)
    finally:temporary.unlink(missing_ok=True)

def read_optional(path):
    # Only absence is pending. Committed syntax/IO errors propagate immediately.
    try:value=read_json(path)
    except FileNotFoundError:return None
    if not isinstance(value,dict):raise IntegrityError('committed record must be an object')
    return value

def control_present(path,expected):
    value=read_optional(path)
    if value is None:return False
    if value!=expected:raise IntegrityError('invalid committed control record')
    return True
