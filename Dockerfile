ARG RUNTIME=3.7

FROM python:${RUNTIME} AS install
RUN pip install pipenv==2018.11.26
WORKDIR /var/task/
COPY Pipfile* /var/task/
RUN pipenv lock -r > requirements.txt
RUN pipenv lock -r -d > requirements-dev.txt
RUN pip install -r requirements.txt -r requirements-dev.txt

FROM install AS build
COPY . .
COPY --from=install /var/task/ .
ARG SETUPTOOLS_SCM_PRETEND_VERSION
ENV SETUPTOOLS_SCM_PRETEND_VERSION ${SETUPTOOLS_SCM_PRETEND_VERSION}
RUN pip install . --no-deps
RUN flake8
RUN py.test
RUN python setup.py sdist
