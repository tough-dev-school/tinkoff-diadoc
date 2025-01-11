# Python version must be set explicitly with build args
ARG PYTHON_VERSION=python-version-not-set

FROM python:${PYTHON_VERSION}-slim-bullseye

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /src

ADD src/ .

ENTRYPOINT ["python", "entrypoint.py"]
