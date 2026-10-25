# AI-Generated Code Review Benchmark

How often does LLM-written Python actually work — and *why* does it fail?

## What I did
1. Built a benchmark of **[N] DSA problems**, each with hand-picked edge-case and performance tests (`problems.json`).
2. Had **[model A]** and **[model B]** solve every problem.
3. Ran every solution in an isolated process with a time limit (`evaluate.py`).
4. **Reviewed every failing solution myself** and classified the bug (`review.py`), with a one-line fix.

## Key findings  (fill from report.md)
- Solve rate: [X]% ([model A]) vs [X]% ([model B])
- Most common bug type: [category] — e.g. ...
- Tests models fail most: [empty input / k > n / performance ...]
- Surprising failure: ...

## Bug patterns  (3–5 in your own words, with code snippet + fix)
1. ...

## Run it
```
pip install -r requirements.txt
set GEMINI_API_KEY=your_key        (Windows cmd)
python generate.py                 # 1. model writes solutions
python evaluate.py                 # 2. run all tests
python review.py                   # 3. YOU review the failures
python report.py                   # 4. numbers -> report.md
```
Second model: `set LLM_PROVIDER=groq` + `set GROQ_API_KEY=...`, then `python generate.py` and re-run evaluate.
