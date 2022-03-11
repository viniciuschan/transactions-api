lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

test:
	poetry run pytest -sx

migrations:
	poetry run python manage.py makemigrations

migrate:
	docker-compose exec transactions-api su -c "python manage.py migrate"

create_fixtures:
	docker-compose exec transactions-api su -c "python manage.py loaddata categories.json"
	docker-compose exec transactions-api su -c "python manage.py loaddata customers.json"
	docker-compose exec transactions-api su -c "python manage.py loaddata transactions.json"

shell:
	docker-compose exec transactions-api su -c "pip install ipython && python manage.py shell"

run:
	docker-compose up -d
