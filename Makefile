.PHONY: format lint test

format:
black .

lint:
flake8 src tests || true

test:
python pytest.py -v
