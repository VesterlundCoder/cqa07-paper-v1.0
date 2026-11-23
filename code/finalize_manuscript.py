"""Check a completed numerical run and generate manuscript values from its data."""
import hashlib
import json
import math
import pathlib

root=pathlib.Path(__file__).resolve().parents[1]
data=root/"data"
log=(root/"logs/run_all.log").read_text()
assert "run_all exit_status=0" in log,"Numerical pipeline has not finished successfully"
runtime=json.loads((data/"runtime.json").read_text())
for name,sha in runtime["code_sha256"].items():
    assert hashlib.sha256((root/"code"/name).read_bytes()).hexdigest()==sha,name
single=json.loads((data/"single_copy.json").read_text())
assert single["S1_0"]=={"numerator":15,"denominator":16,"strategy_pairs_enumerated":65536}
cover=json.loads((data/"covering.json").read_text())["results"]
assert [x["best_cover_size"] for x in cover[:5]]==[2,3,5,8,12]
assert all(x["proven_optimal"] and x["cover_verified"] for x in cover[:5])
assert not cover[5]["proven_optimal"],"If n=6 is now solved, update the text before finalizing"
protocol=json.loads((data/"protocol_check.json").read_text())
assert len(protocol)==5 and all(x["failures"]==0 for x in protocol)
assert sum(x["input_pairs_tested"] for x in protocol)==1118480
heuristic=json.loads((data/"no_comm_n2.json").read_text())
assert heuristic["best_wins"]==227
exact=json.loads((data/"no_comm_n2_exact.json").read_text())
assert "independently_rescored_incumbent_wins" in exact,"Stale supplied solver data"
assert exact["status_code"] in (0,1)
assert exact["upper_bound_wins"] is not None
# At an integral strategy assignment the optimal z values are win bits,
# hence the maximum score is integral. Add tolerance before rounding down.
upper=min(256,math.floor(exact["upper_bound_wins"]+1e-6))
assert upper>=max(227,exact["independently_rescored_incumbent_wins"])
status="optimal" if exact["proven_optimal"] else "time limit reached"
values={"CoverSixIncumbent":cover[5]["best_cover_size"],"CoverSixLower":int(cover[5]["dual_bound"]),
        "NtwoHeuristic":heuristic["best_wins"],"NtwoIncumbent":exact["independently_rescored_incumbent_wins"],
        "NtwoUpper":upper,"NtwoStatus":status}
text="% Generated from the completed archived numerical run; do not edit by hand.\n"
text+="".join("\\newcommand{\\"+name+"}{"+str(value)+"}\n" for name,value in values.items())
(root/"manuscript/computed_values.tex").write_text(text)
verification={"status":"passed","protocol_input_pairs":1118480,"manuscript_values":values,
              "bound_rule":"floor(raw solver upper bound + 1e-6), capped at 256; the strategy score is integral",
              "data_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in data.glob("*.json") if p.name!="verification.json"},
              "finalizer_sha256":hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
(data/"verification.json").write_text(json.dumps(verification,indent=2)+"\n")
print(json.dumps(verification["manuscript_values"],indent=2))
