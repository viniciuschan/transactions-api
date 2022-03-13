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

3. You can check all test cases by running:
```
make test
```

4. To start the service using docker-compose run the following command:
```
make run
```

5. As soon as your containers are up, you must migrate the data structure:
```
make migrate
```

6. I prepared a fixture file to load initial items for testing purposes:
```
make create_fixtures
```


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
    "category": "category_name",
    "user_email": "dev@example.com",
}
```

#### UPDATE

Endpoint: **/v1/transactions/<uuid>/**

Body contract:
```
{
    "reference": "0000000000001",
    "date": "2020-03-01",
    "amount": "5000.00",
    "type": "inflow",
    "category": "category_name",
    "user_email": "dev@example.com",
}
```

#### LIST

Endpoint: **/v1/transactions/**

Response:
```
[
    {
        "id": "9b140ab4-6805-43fa-bb0b-c3b0cc869ba8",
        "reference": "00001",
        "date": "2022-03-01",
        "amount": "1000.00",
        "type": "inflow",
        "category": "category1",
        "user_email": "dev1@test.com"
    },
    {
        "id": "cfade2c7-40cc-4e07-bcd2-82a5b1d99404",
        "reference": "00002",
        "date": "2022-02-10",
        "amount": "-100.00",
        "type": "outflow",
        "category": "category1",
        "user_email": "dev1@test.com"
    }
]
```

#### GET

Endpoint: **/v1/transactions/<uuid>/**

Response:
```
{
    "id": "9b140ab4-6805-43fa-bb0b-c3b0cc869ba8",
    "reference": "00001",
    "date": "2022-03-01",
    "amount": "1000.00",
    "type": "inflow",
    "category": "category1",
    "user_email": "dev1@test.com"
}
```

#### BULK CREATE

Endpoint: **/v1/transactions/bulk/**

Body contract:
```
[
    {
        "reference": "123",
        "date": "2020-01-03",
        "amount": "100.00",
        "type": "inflow",
        "category": "dev1",
        "user_email": "dev1@test.com"
    },
    {
        "reference": "321",
        "date": "2020-03-10",
        "amount": "100.00",
        "type": "outflow",
        "category": "dev1",
        "user_email": "dev1@test.com"
    }
]
```

## How to consult total flow per user

Method: GET

Endpoint: **/v1/transactions/group-by-user/**

Response content:
```
[
    {
        "user_email": "dev1@test.com",
        "total_inflow": 1100.0,
        "total_outflow": -650.0
    },
    {
        "user_email": "dev2@test.com",
        "total_inflow": 100000.0,
        "total_outflow": 0.0
    }
]
```

## How to consult a summary of transactions by user and categories

Method: GET

Endpoint: **/v1/transactions/summary/?user_email=dev@test.com**

Response content:
```
{
    "inflow": {
        "salary": "2500.00",
        "savings": "150.72",
    },
    "outflow": {
        "groceries": "-51.13",
        "rent": "-560.00",
        "transfer": "-150.72",
    }
}
```

=============
