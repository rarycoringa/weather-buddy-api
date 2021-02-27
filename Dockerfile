FROM python:3.8-alpine

WORKDIR /devgrid

RUN apk update && \
    apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /devgrid

CMD ["flask", "run", "--host", "0.0.0.0"]
