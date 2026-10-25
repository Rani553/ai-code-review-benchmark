"""Step 1: ask the model to solve every problem; saves solutions/<model>/<id>.py
Usage: python generate.py [model_name]"""
import json, os, re, sys
from llm import ask, model_name

model = sys.argv[1] if len(sys.argv) > 1 else None
folder = os.path.join("solutions", re.sub(r"[^\w.-]", "_", model_name(model)))
os.makedirs(folder, exist_ok=True)

for p in json.load(open("problems.json")):
    path = os.path.join(folder, p["id"] + ".py")
    if os.path.exists(path):
        continue
    prompt = (f"Solve this in Python.\n\n{p['statement']}\n\nUse exactly this signature:\n{p['signature']}\n\n"
              "Return only the code in one ```python block. No explanation, no example usage.")
    reply = ask(prompt, model)
    m = re.search(r"```(?:python)?\n(.*?)```", reply, re.S)
    open(path, "w", encoding="utf-8").write(m.group(1) if m else reply)
    print("saved", path)
