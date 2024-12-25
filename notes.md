python setup.py build_frontend sdist bdist_wheel
pip install dist/preswald-0.1.0.tar.gz
preswald run preswald_project/hello.py