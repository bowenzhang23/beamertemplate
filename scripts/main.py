import sys
import argparse
import pkgutil
import importlib

sys.path.append("src")

from beamert.compile import BeamerCompiler
import templates


def main(args):
    m = None
    for mo in pkgutil.iter_modules(["scripts/templates"]):
        if mo.name == args.module:
            m = importlib.import_module(f"templates.{mo.name}")
    if m:
        compiler = BeamerCompiler(
            getattr(m, "components"), verbose=args.verbose, force=args.force
        )
        compiler.compile(args.output)
    else:
        print(f"No module named \"{args.module}\", exit..")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "output",
        type=str,
        default="example.tex",
        help="The path to the output tex file.",
    )

    parser.add_argument(
        "-m",
        "--module",
        type=str,
        required=True,
        help="The module that cotains components to import.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show verbose print-outs.",
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force to update the tex file.",
    )

    args = parser.parse_args()
    main(args)
