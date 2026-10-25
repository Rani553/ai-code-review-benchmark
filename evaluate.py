"""Step 2: run all tests on all generated solutions -> results.csv
Usage: python evaluate.py"""
import csv, json, os, subprocess, sys

TIMEOUT = 3  # seconds per test
problems = json.load(open("problems.json"))
rows = []
for model in sorted(os.listdir("solutions")):
    for p in problems:
        sol = os.path.join("solutions", model, p["id"] + ".py")
        if not os.path.exists(sol):
            continue
        for i, t in enumerate(p["tests"]):
            try:
                out = subprocess.run([sys.executable, "runner.py", sol, p["id"], json.dumps(t)],
                                     capture_output=True, text=True, timeout=TIMEOUT)
                res = json.loads(out.stdout.strip().splitlines()[-1]) if out.stdout.strip() \
                      else {"status": "error", "got": out.stderr[-200:]}
            except subprocess.TimeoutExpired:
                res = {"status": "timeout", "got": f">{TIMEOUT}s"}
            rows.append({"model": model, "problem": p["id"], "test": i, "note": t.get("note", ""),
                         "status": res["status"], "expected": str(t["expected"])[:100], "got": res["got"]})
        status = "PASS" if all(r["status"] == "pass" for r in rows if r["model"] == model and r["problem"] == p["id"]) else "FAIL"
        print(f"{model:35} {p['id']:28} {status}")

with open("results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)
print("Saved results.csv")
