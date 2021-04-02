FROM alpine:3.13

WORKDIR /app

RUN apk add --no-cache make build-base jpeg-dev zlib-dev
RUN apk add --no-cache python3 python3-dev py3-pip
RUN apk add --no-cache ffmpeg
COPY ./ /app/
RUN pip3 install -r requirements.txt

CMD ["python3", "./main.py"]