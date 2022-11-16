# tinkoff-diadoc
Должен:
1. Получать выписку платежей из Тинькофф Банк за предыдущий день и находить платежи от юр. лиц
2. Смотреть есть ли юр. лицо в списке контрагентов в Диадок, можно ли ему отправить приглашение
3. Отправлять приглашения, если юр. лицо может работать через Диадок и ещё не в списке наших партнеров  

## Configuration
Configuration should be stored in `src/.env`, for examples see `.env.example`


## Installing on a local machine
This project requires python 3.10.
Deps are managed by [pip-tools](https://github.com/jazzband/pip-tools) with requirements stored in [pyproject.toml](https://github.com/jazzband/pip-tools#requirements-from-pyprojecttoml).

Install and activate virtual environment, like:
```bash
python3 -m venv venv
source venv/bin/activate
cp .env.example ./src/.env  # default environment variables
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
