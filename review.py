"""Step 3 (YOUR work): for every failing solution, read the code and classify the bug.
Usage: python review.py      (resumes; q to quit)"""
import csv, json, os
import pandas as pd

CATS = ["edge_case_missed", "off_by_one", "wrong_algorithm", "too_slow", "crash_exception",
        "misread_problem", "wrong_output_format", "test_is_wrong"]
res = pd.read_csv("results.csv").fillna("")
problems = {p["id"]: p for p in json.load(open("problems.json"))}
failed = res[res["status"] != "pass"].groupby(["model", "problem"])

done = set()
if os.path.exists("reviews.csv"):
    done = {(r["model"], r["problem"]) for r in csv.DictReader(open("reviews.csv", encoding="utf-8"))}
new = not os.path.exists("reviews.csv")

with open("reviews.csv", "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["model", "problem", "category", "explanation", "fix"])
    for (model, pid), g in failed:
        if (model, pid) in done:
            continue
        print("\n" + "=" * 70 + f"\n{model} | {pid}\n{problems[pid]['statement']}\n")
        print(open(os.path.join("solutions", model, pid + ".py"), encoding="utf-8").read())
        print("Failing tests:")
        for _, r in g.iterrows():
            print(f"  test {r['test']} ({r['note']}): {r['status']} expected={r['expected']} got={r['got']}")
        for i, c in enumerate(CATS, 1):
            print(f"  {i}. {c}")
        ch = input("Bug category (q to quit): ").strip()
        if ch == "q":
            break
        expl = input("Why does it fail? (your own words): ").strip()
        fix = input("What is the fix? (one line): ").strip()
        w.writerow([model, pid, CATS[int(ch) - 1], expl, fix])
        f.flush()
print("Saved reviews.csv")
