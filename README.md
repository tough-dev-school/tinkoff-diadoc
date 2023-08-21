# tinkoff-diadoc
Отправляет приглашения в ЭДО Диадок компаниям, которые оплатили нам что-нибудь.

Принцип:
1. Запускается в начале каждого часа
2. Получает список юр. лиц которые что-то оплатили из выписки Тинькофф Банк за предыдущий день
3. Получает список контрагентов в Диадок
4. Отправляет приглашения в Диадок компаниям из списка входящих платежей Тинькофф, если:
    - компания работает через Диадок
    - компании нет в списке наших контрагентов и не отправляли приглашение ранее
    - сообщения вместе с приглашением по умолчанию не отправляется. Можно задать сообщение переменной окружения `MESSAGE_TO_ACQUIRE_COUNTERAGENT`

## Необходимый доступ к API
1. [Тинькофф API](https://business.tinkoff.ru/openapi/docs). Токен должен быть выпущен с доступом:
    1. Информация об операциях компании
    2. Информация о счетах компании
    3. Информация о компании

2. [Диадок API](https://developer.kontur.ru/Docs/diadoc-api/index.html). В решении используем авторизацию по логину-паролю
    1. Diadoc Client ID оформляется через [заявку](https://kontur.ru/diadoc/order) и поддержку Диадок
    2. У Диадока нет разграничений доступа к API. Используйте логин-пароль пользователя с минимальными правами. Для работы нужен доступ "ManageCounteragents"
    3. Доступ к API платный, но на 1-2 недели поддержка может сделать тестовый доступ


## Configuration
Configuration should be stored in `src/.env`, for examples see `env.example`


## Installing on a local machine
This project requires python 3.11
Deps are managed by [pip-tools](https://github.com/jazzband/pip-tools) with requirements stored in [pyproject.toml](https://github.com/jazzband/pip-tools#requirements-from-pyprojecttoml).

Install and activate virtual environment, like:
```bash
python3 -m venv venv
source venv/bin/activate
cp env.example ./src/.env  # default environment variables
```

Install requirements:

```bash
pip install --upgrade pip pip-tools
make  # compile and install deps
```

Format code with isort and black:
```bash
make fmt
```

Run linters
```bash
make lint
```

Run tests
```bash
make test
```
