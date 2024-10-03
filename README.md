# api de crypto moeda assincrona com fastapi
cadastra um usuario de forma simples sem autenticacao adiciona moedas favoritas e traz uma cotacao do dia anterior de todas moedas favoritas

### dependencias

python 3.12

poetry

### bibliotecas utilizadas

* fastapi = "^0.115.0"

* uvicorn = "^0.31.0"

* sqlalchemy = "^2.0.35"

* asyncpg = "^0.29.0"

*  aiohttp = "^3.10.8"

### como rodar

` git clone https://github.com/Romariolima1998/fastapi_crypto.git `

` cd fastapi_crypto `

` poetry install `

` cd crypto `

` uvicorn main:api --port 8000 `

