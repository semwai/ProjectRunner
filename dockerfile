FROM python:3.10 as builder

RUN pip install pipenv

WORKDIR /app

COPY Pipfile* .

COPY . .

RUN pipenv requirements > requirements.txt

FROM python:3.10-alpine

WORKDIR /app

COPY --from=builder /app /app

ENV PYTHONPATH="/app/"

RUN pip install -r requirements.txt

WORKDIR /app/runner/example/web_project

EXPOSE 8000

ENTRYPOINT ["python", "app.py"]