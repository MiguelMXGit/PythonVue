FROM alpine:3.10

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /Project

COPY . /Project

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3", "server/app.py"]