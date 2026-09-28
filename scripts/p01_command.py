"""Save one command's real output, exit and duration to a new log."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

path = Path(sys.argv[1])
if path.exists(): raise RuntimeError('log exists')
command=sys.argv[2:]
start=time.perf_counter()
timestamp=datetime.now(timezone.utc).isoformat()
env=os.environ.copy()
env['PYTHONUTF8']='1'
p=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',errors='replace',env=env)
record={'evidence_kind':'development_observation','timestamp_utc':timestamp,'argv':command,
        'exit':p.returncode,'seconds':time.perf_counter()-start,
        'stdout':p.stdout.replace(str(Path.home()),'<home>'),
        'stderr':p.stderr.replace(str(Path.home()),'<home>')}
path.parent.mkdir(parents=True,exist_ok=True)
with path.open('x',encoding='utf-8',newline='\n') as f: json.dump(record,f,indent=2)
print(json.dumps({'log':str(path),'exit':p.returncode,'seconds':record['seconds'],
                  'stdout_tail':record['stdout'][-1500:],'stderr_tail':record['stderr'][-1500:]}))
raise SystemExit(p.returncode)
