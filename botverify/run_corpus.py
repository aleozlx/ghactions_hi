import json, os, subprocess, sys

cases = json.load(open("botverify/corpus/manifest.json"))
# Append the real #4880 comments.
real_expect = {"c00":"run","c03":"run","c04":"run","c06":"run","c07":"run","c08":"run","c10":"run",
               "c01":"unknown","c02":"unknown","c05":"unknown","c09":"unknown"}
for f in sorted(os.listdir("botverify/corpus4880")):
    if not f.endswith(".txt"): continue
    key = f.split("_")[0]
    cases.append({"name": f"REAL_{f[:-4]}", "expect": real_expect[key],
                  "body": open(os.path.join("botverify/corpus4880", f)).read()})

def run(script, body):
    return subprocess.run(["bash", script], input=body, capture_output=True, text=True).stdout.strip()

rows, fails = [], 0
for c in cases:
    old = run("botverify/parse_old.sh", c["body"])
    new = run("botverify/parse_live.sh", c["body"]).replace("command=","")
    ok = (new == c["expect"])
    if not ok: fails += 1
    rows.append((c["name"], c["expect"], old, new, "PASS" if ok else "FAIL"))

w = max(len(r[0]) for r in rows)
print(f"{'case'.ljust(w)}  {'expected':<13} {'old':<13} {'new':<13} result")
print("-" * (w + 50))
for r in rows:
    print(f"{r[0].ljust(w)}  {r[1]:<13} {r[2]:<13} {r[3]:<13} {r[4]}")

old_wrong = sum(1 for r in rows if r[2] != r[1])
print(f"\ncases={len(rows)}  new-failures={fails}  old-would-have-been-wrong-on={old_wrong}")
sys.exit(1 if fails else 0)
