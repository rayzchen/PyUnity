import os
import glob
import shutil
import sys
import pkgutil
if "cython" not in os.environ:
    os.environ["cython"] = "1"

if len(sys.argv) < 2:
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
            "[![Python version](https://img.shields.io/pypi/pyversions/pyunity.svg?logo=python&logoColor=FBE072)]",
            "(https://pypi.python.org/pypi/pyunity) ",
            "[![Commits since last release](https://img.shields.io/github/commits-since/rayzchen/pyunity/",
            "0.2.1.svg)](https://github.com/rayzchen/pyunity/compare/0.2.1...master)",
            "[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/rayzchen/pyunity.svg",
            "?logo=lgtm)](https://lgtm.com/projects/g/rayzchen/pyunity/context:python)",
            # "[![Travis Build Status](https://travis-ci.org/rayzchen/pyunity.svg?branch=master)]",
            # "(https://travis-ci.org/rayzchen/pyunity)",
            "[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/ohl61d2vavl37tmj?svg=true)]",
            "(https://ci.appveyor.com/project/rayzchen/pyunity)",
        ])
    ]
    skip = 0
    for i in range(len(desc)):
        if skip:
            skip = 0
            continue
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
    if pkgutil.find_loader("cython") is None:
        raise Exception("Cython is needed to create CPython extensions.")
    if os.path.exists("src"):
        shutil.rmtree("src")
    pxd_files = glob.glob("ext/**/*.pxd", recursive=True)
    for f in pxd_files:
        shutil.copy(f, os.path.join("pyunity", f[4:]))
    for path in glob.glob("pyunity/**/*.*", recursive=True):
        if path.endswith(".pyc") or path.endswith(".pxd"):
            continue
        dirpath, file = os.path.split(path)
        print(file)
        if file.endswith(".py") and not file.startswith("__"):
            loc = os.getcwd()
            os.chdir(dirpath)
            code = os.system("cythonize -3 -q " + file)
            os.chdir(loc)
            srcPath = os.path.join(dirpath, file)[:-2] + "c"
            if code != 0:
                os.remove(srcPath)
                break
            op = shutil.move
        else:
            srcPath = os.path.join(dirpath, file)
            op = shutil.copy
        destPath = os.path.join("src", os.path.dirname(srcPath[8:]))
        os.makedirs(destPath, exist_ok=True)
        op(srcPath, destPath)
    for f in pxd_files:
        os.remove(os.path.join("pyunity", f[4:]))
