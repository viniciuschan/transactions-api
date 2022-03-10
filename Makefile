lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

test:
	poetry run pytest -sx

run:
	poetry run python manage.py runserver

migrations:
	docker-compose exec transactions-api su -c "python manage.py makemigrations"

migrate:
	docker-compose exec transactions-api su -c "python manage.py migrate"

create_fixtures:
	docker-compose exec transactions-api su -c "python manage.py loaddata categories.json"
	docker-compose exec transactions-api su -c "python manage.py loaddata customers.json"
	docker-compose exec transactions-api su -c "python manage.py loaddata transactions.json"
