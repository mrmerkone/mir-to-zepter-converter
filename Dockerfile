# syntax=docker/dockerfile:1
FROM node:slim AS front-bulder

COPY frontend/ ./

RUN npm install && npm run build

FROM python:3.10-slim AS app
WORKDIR /usr/src/app

ENV PYTHONPATH=/usr/src/app/src/:$PYTHONPATH

COPY ./backend/pyproject.toml ./
COPY ./backend/src ./src
COPY --from=front-bulder dist/ ./dist

RUN pip install -U poetry
RUN poetry install

CMD ["poetry", "run", "python", "-m", "app"]