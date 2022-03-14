# Development shortcuts
lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

migrations:
	poetry run python manage.py makemigrations

migrate:
	docker-compose exec transactions-api su -c "python manage.py migrate"

test:
	docker-compose exec transactions-api su -c "poetry run pytest -sx"

load_data:
	docker-compose exec transactions-api su -c "python manage.py shell < script_load_test_data.py"

shell:
	docker-compose exec transactions-api su -c "pip install ipython && python manage.py shell"

run:
	docker-compose up

drop:
	docker-compose down


# Heroku shortcuts
logs:
	heroku logs --app belvo-transactions-api --tail

prod_shell:
	heroku run --app belvo-transactions-api "pip install ipython && python manage.py shell"

deploy:
	git push heroku main
	@echo "Application deployed with success!"

get-env:
	heroku config:get $(ENV)

set-env:
	heroku config:set $(ENV)=$(VALUE)

heroku-migrate:
	heroku run python manage.py migrate
