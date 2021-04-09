FROM python:3.8-alpine

WORKDIR /devgrid

RUN apk update && \
    apk add --no-cache gcc musl-dev linux-headers

COPY . /devgrid
RUN pip3 install -U pipenv
RUN pipenv install --deploy

CMD ["pipenv", "run", "flask", "run", "--host", "0.0.0.0"]
