[![CircleCI](https://circleci.com/gh/viniciuschan/transactions-api/tree/main.svg?style=svg&circle-token=d1bb25356a754041bf1e1c454930ebdb89d94134)](https://circleci.com/gh/viniciuschan/transactions-api/tree/main)

Check my APP: https://belvo-transactions-api.herokuapp.com/

# Transactions API
=============
##### API Rest to deal with financial transactions
###### Author: Vinícius Chan

#### Required dependencies

| Dependency | Download Link |
| ------ | ------ |
| Docker | https://www.docker.com/ |
| Docker-Compose | https://docs.docker.com/compose/ |
| Python 3.10+ | https://www.python.org/downloads/release/python-3102/ |

# Getting Started

I prepared an easy way to run this project locally:

1. Clone this repository:
```
git clone git@github.com:viniciuschan/transactions-api.git
```

2. In the project root directory, there are some useful Makefile commands.

3. To start the service using docker-compose run the following command:
```
make run
```

4. As soon as your containers are up, you must migrate the data structure:
```
make migrate
```

5. You can check all test cases by running:
```
make test
```

6. I prepared a script to load 3.2M transactions records for testing purposes. This is the command:
```
make load_data
```

* PS: On my computer it took about 4~5 min for loading all the test database.


=============


# About the project: How it works

## Manipulating transactions
#### POST

Endpoint: **/v1/transactions/**

Body contract:
```
{
    "reference": "0000000000001",
    "date": "2022-03-01",
    "amount": "1000.00",
    "type": "inflow",
    "category": "category-name",
    "user_email": "dev@example.com"
}
```

#### LIST

Endpoint: **/v1/transactions/**

Response:
```
{
    "count": 240004,
    "next": "http://127.0.0.1:8000/v1/transactions/?page=2",
    "previous": null,
    "results": [
        {
            "id": "c748798a-6110-4466-90cc-35360773a745",
            "reference": "0",
            "date": "2022-10-10",
            "amount": "100.00",
            "type": "inflow",
            "category": "category-A",
            "user_email": "dev@test.com"
        },
        {
            "id": "1880b4e3-2223-4bf2-901b-6d965a331bdd",
            "reference": "1600000",
            "date": "2022-10-10",
            "amount": "1000.00",
            "type": "inflow",
            "category": "category-B",
            "user_email": "dev@test.com"
        }
    ]
{
```

#### GET

Endpoint: **/v1/transactions/uuid/**

Response:
```
{
    "id": "c748798a-6110-4466-90cc-35360773a745",
    "reference": "123",
    "date": "2022-10-10",
    "amount": "100.00",
    "type": "inflow",
    "category": "category-A",
    "user_email": "dev@test.com"
}
```

#### BULK CREATE

Endpoint: **/v1/transactions/bulk/**

Body contract:
```
[
    {
        "reference": "99999999",
        "date": "2020-01-03",
        "amount": "100.00",
        "type": "inflow",
        "category": "category-B",
        "user_email": "dev2@test.com"
    },
    {
        "reference": "999999999999999",
        "date": "2020-03-10",
        "amount": "-100.00",
        "type": "outflow",
        "category": "category-C",
        "user_email": "dev2@test.com"
    }
]
```

## How to filter a transaction by it's reference code

Method: GET

Endpoint: **/v1/transactions/?search=800001**

Response content:
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "929d4f05-b52e-4351-95b9-24bdebc292b5",
            "reference": "800001",
            "date": "2022-10-10",
            "amount": "-100.00",
            "type": "outflow",
            "category": "category-A",
            "user_email": "dev@test.com"
        }
    ]
}
```

## How to consult total flow amount per user

Method: GET

Endpoint: **/v1/transactions/group-by-user/**

Response content:
```
[
    {
        "user_email": "dev2@test.com",
        "total_inflow": "100.00",
        "total_outflow": "-100.00"
    },
    {
        "user_email": "dev@test.com",
        "total_inflow": "879451100.00",
        "total_outflow": "-879451100.00"
    }
]
```

## How to consult a summary of transactions amount by categories per user

Method: GET

Endpoint: **/transactions/summary/?user_email=dev@test.com**

Response content:
```
{
    "inflow": {
        "category-A": "79950100.00",
        "category-B": "799501000.00"
    },
    "outflow": {
        "category-A": "-79950100.00",
        "category-B": "-799501000.00"
    }
}
```

## Swagger Documentation

Endpoint: **/v1/docs**


=============

## Some important considerations about this implementation:

* In bulk create, if you pass a list of transactions with duplicate reference values, only the first one will be created and the rest will be silently discarded. (logged as warning);

* Still in bulk create, if a transaction already exists in database, when trying to create another one with the same reference key, the duplicated item will be discarded and the stored item will be kept unchanged. However, if you pass any invalid item in the bulk create list of items, the entire transaction will be aborted and no item will be created.

* PATCH AND PUT operations have been disabled to maintain transactions integrity;

* Added soft-delete for transaction's model, so it can be safely deleted;

* When creating a transaction, if the corresponding user does not exist in the database, a new one will be created.

* Because it is an API, I added the DRF throttling functionality. The rate limit values ​​can be controlled by environment variable;

* Added logs to map exception cases in serializer validations;

* For convenience, I created a simple customer model. But I could have extended django's django.contrib.auth.User class if I needed better access control.

* Also for convenience, I created some implementations within a single app and single files, but in production it might make sense to separate them into different apps.

* For the Transaction.type attribute I tested a models.SmallIntegerField() with db_index=True and the queries had practically the same result as storing the strings "inflow" and "outflow". So I decided to leave it that way for convenience.

* I did some load tests with approximately 3.2M database registers for a given user. The "summary" and "group-by-user" queries presented good performance (+- 500ms).

* PS*: I should have configured the project with Pipenv instead of Poetry, so heroku would consider pipfile.lock. As I used poetry, I needed to generate a requirements.txt in the root so that the project could be recognized by the Heroku builder.

Well, I put a lot of effort into this project.

I hope you enjoy it =]
