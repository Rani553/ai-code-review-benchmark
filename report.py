"""Step 4: numbers for README/resume -> report.md"""
import os
import pandas as pd

res = pd.read_csv("results.csv")
per_problem = res.groupby(["model", "problem"])["status"].apply(lambda s: (s == "pass").all()).reset_index(name="solved")
lines = ["# Results\n", "## Solve rate by model\n",
         per_problem.groupby("model")["solved"].agg(["sum", "count", "mean"])
         .rename(columns={"sum": "solved", "count": "problems", "mean": "rate"}).round(2).to_markdown(),
         "\n## Failing tests by type\n", res[res["status"] != "pass"]["status"].value_counts().to_markdown(),
         "\n## Edge-case tests failed (by note)\n",
         res[(res["status"] != "pass") & res["note"].notna()]["note"].value_counts().to_markdown()]

if os.path.exists("reviews.csv"):
    rv = pd.read_csv("reviews.csv")
    lines += ["\n## Bug categories (my review)\n", rv["category"].value_counts().to_markdown(), "\n## Bugs\n"]
    for _, r in rv.iterrows():
        lines.append(f"- **{r['problem']}** ({r['model']}) — {r['category']}: {r['explanation']} → fix: {r['fix']}")

open("report.md", "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines[:3]))
print("Full report -> report.md")
