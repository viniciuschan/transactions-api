lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

test:
	poetry run pytest -sx transactions-api

migrate:
	poetry run python transactions-api/manage.py makemigrations
	poetry run python transactions-api/manage.py migrate

run:
	poetry run python transactions-api/manage.py runserver

create_mocks:
	poetry run python transactions-api/manage.py loaddata categories.json
	poetry run python transactions-api/manage.py loaddata customers.json
	poetry run python transactions-api/manage.py loaddata transactions.json
