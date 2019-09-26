sh ./rebuild.sh
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip uninstall -y kcrawler
pip install --index-url https://test.pypi.org/simple/ --no-deps kcrawler
python -c "import kcrawler; kcrawler.main()"
