git pull
pip install cython
python prepare.py
python setup.py bdist_wheel -d dist/0.2.0/
rm -rf build/ pyunity.egg-info/
git add .
git commit -m "Built on linux"
git push