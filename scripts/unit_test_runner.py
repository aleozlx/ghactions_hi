import argparse, sys
p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="op", required=True)
for name in ("run", "plan", "__shell-settings"):
    c = sub.add_parser(name)
    c.add_argument("--test-path", nargs="+", default=["tests/"])
a = p.parse_args(sys.argv[1:])
print("run"); print(" ".join(a.test_path))
