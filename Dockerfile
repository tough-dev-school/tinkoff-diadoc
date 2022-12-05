ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-bullseye

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /src

ADD src/ .

ENTRYPOINT python entrypoint.py
