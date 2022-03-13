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
	docker-compose up

# Heroku development shortcuts
logs:
	heroku logs --app belvo-transactions-api --tail

prod_shell:
	heroku run --app belvo-transactions-api "pip install ipython && python manage.py shell"

deploy:
	poetry export -f requirements.txt -o requirements.txt --without-hashes
	git push heroku main:main
	rm requirements.txt
	echo "deployed with success!"

get-env:
	heroku config:get $(ENV)

set-env:
	heroku config:set $(ENV)=$(VALUE)

heroku-migrate:
	heroku run python manage.py migrate
