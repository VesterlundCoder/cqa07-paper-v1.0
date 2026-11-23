#!/usr/bin/env bash
# Recompute this work's results and figures; literature values remain cited inputs.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p ../logs
exec > >(tee ../logs/run_all.log) 2>&1
trap 'code=$?; printf "run_all exit_status=%s finished_utc=%s\n" "$code" "$(date -u +%FT%TZ)"' EXIT
printf 'started_utc=%s\n' "$(date -u +%FT%TZ)"
python3 - <<'PY'
import hashlib, importlib.metadata, json, pathlib, platform, sys
root=pathlib.Path.cwd().parent
manifest={"python":sys.version,"platform":platform.platform(),
          "packages":{p:importlib.metadata.version(p) for p in ["numpy","scipy","matplotlib"]},
          "code_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root/"code").glob("*")) if p.is_file()}}
(root/"data/runtime.json").write_text(json.dumps(manifest,indent=2)+"\n")
print("Runtime:",manifest["python"],manifest["packages"])
PY
for script in single_copy.py "covering_ilp.py 6 120" "protocol_check.py 5" no_comm_n2.py "no_comm_n2_exact.py 1200" make_figures.py; do
  printf '\nRunning %s\n' "$script"
  # Each entry is a fixed script/argument list above, never user-supplied shell code.
  read -r -a command_args <<< "$script"
  python3 -u "${command_args[@]}" 2>&1 | tee "../logs/${command_args[0]%.py}.log"
done
