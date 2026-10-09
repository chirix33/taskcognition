"""Publish once after offline source/tests stabilize; never authorizes execution."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.metadata,json
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash
from taskcognition.p02d_plan import PLAN_DIR,RUN,VERSION,LIMITS,validate_plan
from taskcognition.p02d_features import FEATURE_SPEC

def candidate(root):
    directory=root/PLAN_DIR
    bound={p.relative_to(root).as_posix():file_hash(p) for base in (directory,root/'src/taskcognition',root/'vendor/reasoning_gym_p02a')
           for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='run_plan.json'}
    for n in ('docs/amendments/CR01_2026-10-05_v1.md','docs/PROTOCOL_SOURCE_OF_TRUTH.md','docs/STATISTICAL_CONTRACT.md','docs/P02D_RUNNER_CONTRACT.md',
              'reports/p02c/next_development_proposal.md','reports/p01/model_download.json','artifacts/development/p02b-two-cap/package_base.json'):
        bound[n]=file_hash(root/n)
    env=read_json(directory/'environment.json')
    runtime=root/'.venv-inference/Lib/site-packages'
    for path in (runtime/'transformers').rglob('*.py'):
        bound[path.relative_to(root).as_posix()]=file_hash(path)
    for name in ('torch','tokenizers','numpy','transformers'):
        dist=importlib.metadata.distribution(name)
        for f in dist.files or []:
            if str(f).endswith('.dist-info/RECORD'):
                p=Path(dist.locate_file(f));bound[p.relative_to(root).as_posix()]=file_hash(p)
    return dict(evidence_kind='development_observation',split='DEVELOPMENT',phase='P02D',specification_version=VERSION,
        plan_version='P02D-offline-v4',authorization='PENDING_SEPARATE_RECORD',scientific_freeze=False,completion_policy='descriptive',
        timestamp_utc=datetime.now(timezone.utc).isoformat(),output_directory=RUN,package=read_json(directory/'package.json'),
        inputs=read_json(directory/'inputs.json'),requests=read_json(directory/'answer_schedule.json'),feature_schedule=read_json(directory/'feature_schedule.json'),
        feature_specification=FEATURE_SPEC,environment=env,caps={'D':2048,'R':2048},limits=LIMITS,bound_files=bound,
        initial_counters=dict(answer_dispatches=0,feature_forwards=0,output_tokens_reserved=0,model_loads=0),
        clocks=dict(residency='sum of isolated worker intervals from before spawn to final wait, includes load/warmup/cancellation/cleanup; perf_counter',
            wall='single supervisor invocation perf_counter; no automatic restart; unfinished sessions stop with measured lower bound and unknown remainder',
            packet='reserve a second copy of all raw execution/report bytes plus 16MiB next-event headroom; measure actual packet and overshoot'),
        stop_rules=['no replacement/replay/J=0','any feature partial/timeout/invalid stops before answers','software/evidence error is unscored incident',
            'future single authorization record binds this file SHA; pending state always rejects','reserve 300s per answer, first feature load/forward 300s and each subsequent forward 150s',
            'unknown cleanup blocks further work; all actual overshoot retained','raw outcomes retained regardless of success; no outcome-based stop'],
        unresolved=['final feature freeze','scalar cost choice','beta','hard cost support','final samples/repeats','durable final-study backup'])

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    plan=validate_plan(candidate(root));path=root/PLAN_DIR/'run_plan.json';write_new(path,plan)
    write_new(root/'reports/p02d_correction_v4/plan_receipt.json',dict(evidence_kind='development_observation',plan_path=PLAN_DIR+'/run_plan.json',sha256=file_hash(path),authorization='PENDING',live_dispatch=False))
    print(json.dumps(read_json(root/'reports/p02d_correction_v4/plan_receipt.json')))
