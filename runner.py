"""Runs ONE test in a separate process (so infinite loops / crashes can't kill the benchmark)."""
import importlib.util, json, sys

sol_path, func_name, test_json = sys.argv[1], sys.argv[2], sys.argv[3]
test = json.loads(test_json)
try:
    spec = importlib.util.spec_from_file_location("sol", sol_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    args = eval(test["args_expr"]) if "args_expr" in test else test["args"]
    got = getattr(mod, func_name)(*args)
    got = json.loads(json.dumps(got))          # tuples -> lists, so comparison is fair
    print(json.dumps({"status": "pass" if got == test["expected"] else "wrong",
                      "got": str(got)[:200]}))
except Exception as e:
    print(json.dumps({"status": "error", "got": f"{type(e).__name__}: {e}"[:200]}))
