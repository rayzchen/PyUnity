import os, glob, shutil, sys
if "cython" not in os.environ: os.environ["cython"] = "1"

if len(sys.argv) == 1:
    import pyunity
    desc = pyunity.__doc__.split("\n")
    desc_new = [
        "# PyUnity", "",
        "".join([
            "[![Documentation Status](https://readthedocs.org/projects/pyunity/badge/?version=latest)]",
            "(https://pyunity.readthedocs.io/en/latest/?badge=latest) ",
            "[![License](https://img.shields.io/pypi/l/pyunity.svg?v=1)]",
            "(https://pypi.python.org/pypi/pyunity)",
            "[![PyPI version](https://img.shields.io/pypi/v/pyunity.svg?v=1)]",
            "(https://pypi.python.org/pypi/pyunity) ",
            "[![Python version](https://img.shields.io/badge/python-3-blue.svg?v=1)]",
            "(https://img.shields.io/badge/python-3-blue.svg?v=1) ",
            "[![Commits since last release](https://img.shields.io/github/commits-since/rayzchen/pyunity/",
            "0.1.0.svg)](https://github.com/rayzchen/pyunity/compare/0.1.0...master)",
            "[![Travis Build Status](https://travis-ci.org/rayzchen/pyunity.svg?branch=master)]",
            "(https://travis-ci.org/rayzchen/pyunity)",
        ])
    ]
    skip = 0
    for i in range(len(desc)):
        if skip: skip = 0; continue
        if i != len(desc) - 1 and len(set(desc[i + 1])) == 1:
            if desc[i + 1][0] == "-":
                desc_new.append("### " + desc[i])
                skip = 1
            elif desc[i + 1][0] == "=":
                desc_new.append("## " + desc[i])
                skip = 1
        else:
            if "create a new pull request" in desc[i]:
                desc[i] = desc[i].replace(
                    "create a new pull request",
                    "[create a new pull request](https://github.com/rayzchen/pyunity/pulls)"
                )
            desc_new.append(desc[i].replace("::", ":"))

    with open("README.md", "w") as f:
        for line in desc_new:
            f.write(line + "\n")

if os.environ["cython"] == "1":
    try:
        import Cython
    except ModuleNotFoundError:
        raise Exception("Cython is needed to create CPython extensions.")
    if os.path.exists("src"): shutil.rmtree("src")
    # pxd_files = glob.glob("ext/**/*.pxd", recursive = True)
    # for f in pxd_files:
    #     shutil.copy(f, os.path.join("pyunity", f[4:]))
    for path in [
            *glob.glob("pyunity/**/*.py", recursive = True),
            *glob.glob("pyunity/**/*.mesh", recursive = True)]:
        dirpath, file = os.path.split(path)
        print(file)
        if file.startswith("__") or file.endswith(".mesh"):
            srcPath = os.path.join(dirpath, file)
            op = shutil.copy
        else:
            loc = os.getcwd()
            os.chdir(dirpath)
            os.system("cythonize -3 -q " + file)
            os.chdir(loc)
            srcPath = os.path.join(dirpath, file)[:-2] + "c"
            op = shutil.move
        destPath = os.path.join("src", os.path.dirname(srcPath[8:]))
        try: os.makedirs(destPath)
        except: pass
        op(srcPath, destPath)
    # for f in pxd_files:
    #     os.remove(os.path.join("pyunity", f[4:]))