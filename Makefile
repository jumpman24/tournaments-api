
install:
	pip install -i https://pypi.python.org/simple/ -Ur requirements.txt

develop:
	pip install -i https://pypi.python.org/simple/ -Ur requirements-dev.txt

migration:
	alembic revision --autogenerate -m "$(name)"

migrate-up:
	alembic upgrade head

migrate-down:
	alembic downgrade -1
