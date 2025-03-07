docker-compose down -v
docker-compose up -d


docker-compose down -v
docker-compose up --build

<img src="/.github/images/xp-inc-logo.png" alt="xp-inc" width=100px>

# XP Inc. | Backend Sênior

Este projeto trata-se de um desafio técnico backend da **XP Inc**. Solucionado como **perfil sênior** usando **Python**.

`Desafio Proposto:` Este projeto contém apenas o Backend da aplicação. Onde simula um aplicativo de investimento em ações, com algumas funcionalidades de conta digital.

## Controle de Token - Design

<img src="/.github/images/design1.png" alt="xp-inc" width=450px>

## Frameworks 🛠️

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [PyTest](https://docs.pytest.org/en/stable/)
- [SlowAPI](https://pypi.org/project/slowapi/)
- [ORJSON](https://github.com/ijl/orjson)
- [Redis](https://redis.io/)
- [Psycopg2](https://www.psycopg.org/)
- Entre outras...

## Endpoints

### Inicio

> **GET** /: Rota inicial.

Não é necessário Authorization.

```json
"Hello World!"
```

> **GET** /ping: Rota para ping.

Não é necessário Authorization.

```json
"Pong!"
```

## Acesso e controle

> **GET** /account: Detalhes da conta.
    
AUTHORIZATION: acess_token

```json
{
    "status": "success",
    "message": "Account details fetched successfully.",
    "account_details": {
        "email": "test@gmail.com",
        "balance": 1000.0,
        "created_at": "2025-03-06T18:23:07.623590"
    },
    "assets": [
        {
            "ticker": "PEP",
            "quantity": 1
        }
    ],
    "datetime": "2025-03-06 20:05:24"
}
```


> **POST** /login: Realiza o login de um cliente. Se os dados estiverem corretos, um token de refresh é gerado e retornado.

Não é necessário Authorization.
    
```json
{
    "email": "client1@example.com",
    "password": "password123"
}
```
    
```json
{
    "status": "success",
    "message": "Client logged in successfully",
    "acess_data": {
        "acess_token": "some_random_token_value",
        "ttl": 3600
    },
    "datetime": "2025-03-06 10:30:00"
}
```

> **POST** /signup: Realiza o cadastro de um novo cliente, salvando seu email, senha e saldo inicial.

```json
{
    "email": "newclient@example.com",
    "password": "newpassword123"
}
```

```json
{
    "status": "success",
    "message": "Client signed up successfully",
    "client_data": {
        "email": "newclient@example.com",
        "balance": 0
    },
    "datetime": "2025-03-06 10:30:00"
}
```

## Finance

AUTHORIZATION: acess_token

> **POST** /deposit: Registra um depósito para um cliente, adicionando um valor ao seu saldo.

```json
{
    "id_user": 123,
    "amount": 150.0
}
```

```json
{
    "status": "success",
    "message": "Deposit successful",
    "transaction_data": {
        "id": 1,
        "id_user": 123,
        "amount": 150.0,
        "transaction_at": "2025-03-06 10:30:00"
    },
    "datetime": "2025-03-06 10:35:00"
}
```

> **POST** /withdraw: Realiza um saque para um cliente, subtraindo um valor do seu saldo.

AUTHORIZATION: acess_token

```json
{
    "id_user": 123,
    "amount": 50.0
}
```
    
```json
{
    "status": "success",
    "message": "Withdraw successful",
    "transaction_data": {
        "id": 1,
        "id_user": 123,
        "amount": 50.0,
        "transaction_at": "2025-03-06 11:00:00"
    },
    "datetime": "2025-03-06 11:05:00"
}
```

> **GET** /transactions: Retorna o histórico de transações (depósitos, saques, transferências) de um cliente.

AUTHORIZATION: acess_token
    
```json
{
    "status": "success",
    "message": "Transaction history fetched successfully.",
    "transaction_history": [
        {
          "id": 1,
          "type": "deposit",
          "amount": 150.0,
          "transaction_at": "2025-03-06 10:30:00"
        },
        {
          "id": 2,
          "type": "withdraw",
          "amount": 50.0,
          "transaction_at": "2025-03-06 11:00:00"
        },
        {
          "id": 3,
          "type": "transfer",
          "amount": 100.0,
          "transaction_at": "2025-03-06 12:00:00"
        }],
    "datetime": "2025-03-06 12:05:00"
}
```

## Mercado de Ações

> **GET** /stockmarket: Retorna o mercado de ações atual.

AUTHORIZATION: acess_token

```json
{
    "status": "success",
    "message": "Current stock market successfully obtained.",
    "email": "test@gmail.com",
    "stockmarket": [
        {
            "id": 1,
            "name": "Apple Inc.",
            "ticker": "AAPL",
            "price": 175.5,
            "quantity": 50,
            "created_at": "2025-03-06T18:21:14.046977"
        },
        {
            "id": 2,
            "name": "Tesla Inc.",
            "ticker": "TSLA",
            "price": 800.25,
            "quantity": 30,
            "created_at": "2025-03-06T18:21:14.046977"
        }],
    "datetime": "2025-03-06 19:57:58"
}
```

> **POST** /stockmarket/buy: Realiza a compra de uma ação dentro do mercado de ações.

AUTHORIZATION: acess_token

### Input

```json
{
    "ticker": "PEP",
    "quantity": 1
}
```

```json
{
    "status": "success",
    "message": "Asset bought successfully",
    "email": "test@gmail.com",
    "stockmarket": {
        "name": "PepsiCo Inc.",
        "ticker": "PEP",
        "quantity": 1
    },
    "datetime": "2025-03-06 19:52:47"
}
```

> **POST** /stockmarket/sell: Realiza a venda de uma ação dentro do mercado de ações.

AUTHORIZATION: acess_token

```json
{
    "ticker": "PEP",
    "quantity": 1
}
```

```json
{
    "status": "success",
    "message": "Asset sold successfully",
    "email": "test@gmail.com",
    "stockmarket": {
        "name": "PepsiCo Inc.",
        "ticker": "PEP",
        "quantity": 4
    },
    "datetime": "2025-03-06 21:00:47"
}
```

## Histórico

> **POST** /deposity-history: Extrato historico de depositos do usuário.

AUTHORIZATION: acess_token

```json
{
    "status": "success",
    "message": "Asset sold successfully",
    "email": "test@gmail.com",
    "stockmarket": {
        "name": "PepsiCo Inc.",
        "ticker": "PEP",
        "quantity": 4
    },
    "datetime": "2025-03-06 21:00:47"
}
```

> **POST** /withdraw-history: Extrato historico de saques do usuário.

AUTHORIZATION: acess_token

```json
{
    "status": "success",
    "message": "Withdraw history fetched successfully.",
    "email": "test@gmail.com",
    "withdraw_history": [
        {
            "id": 1,
            "amount": 1.0,
            "transaction_at": "2025-03-06T19:39:42.367431"
        }],
    "datetime": "2025-03-06 20:04:59"
}
```

## Rotas administrativas

> **GET** /admin/withdraw-history: Extrato historico de saques do usuário.

AUTHORIZATION: 123 (Vicê pode customizar no .env)

```json
{
    "status": "success",
    "message": "Withdraw history fetched successfully.",
    "withdraw_history": [
        {
            "id": 2,
            "id_user": 1,
            "amount": 1.0,
            "transaction_at": "2025-03-06T20:05:11.889990"
        },
        {
            "id": 1,
            "id_user": 1,
            "amount": 1.0,
            "transaction_at": "2025-03-06T19:39:42.367431"
        }
    ],
    "datetime": "2025-03-06 20:13:04"
}
```

> **GET** /admin/deposit-history: Extrato historico de saques do usuário.

AUTHORIZATION: 123 (Você pode customizar no .env)

```json
{
    "status": "success",
    "message": "Deposit history fetched successfully.",
    "withdraw_history": [
        {
            "id": 3,
            "id_user": 1,
            "amount": 1000.0,
            "transaction_at": "2025-03-06T20:05:07.741433"
        }],
    "datetime": "2025-03-06 20:13:01"
}
```

> **GET** /admin/users: Extrato historico de saques do usuário.

AUTHORIZATION: 123 (Vicê pode customizar no .env)

```json
{
    "status": "success",
    "message": "Client history fetched successfully.",
    "client": [
        {
            "id": 1,
            "email": "test@gmail.com",
            "balance": 3719.2,
            "created_at": "2025-03-06T18:23:07.623590"
        }
    ],
    "datetime": "2025-03-06 20:12:56"
}
```
---

# Instalação 📂
> Siga estes passos para instalar e configurar o projeto:

1. Clone o repositório:
    > git clone https://github.com/7Johnsz/Uber-FoodTrucks.git

2. Buildar conteiners utilizando Docker
    > docker-compose up -d 

    E Pronto!