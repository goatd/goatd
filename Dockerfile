FROM python:3-alpine

WORKDIR /build

COPY . ./

COPY ./goatd-config.yaml.example /opt/goatd/config/goatd-config.yaml
COPY ./example/basic_behaviour.py /opt/goatd/behaviours/
COPY ./example/basic_driver.py /opt/goatd/drivers/
COPY ./bin/goatd /usr/local/bin/

# Bind on all adapters so dockers bridge network works as expected
RUN sed -i.bak 's/127\.0\.0\.1/0\.0\.0\.0/' /opt/goatd/config/goatd-config.yaml && \
    rm /opt/goatd/config/goatd-config.yaml.bak

RUN apk update && \
    apk add git && \
    pip3 install -r requirements.txt && \
    python3 setup.py install && \
    git clone https://github.com/goatd/python-goatd.git && \
    cd python-goatd && \
    python3 setup.py install && \
    rm -rf /build

EXPOSE 2222

ENV PYTHONUNBUFFERED 1

ENV CONFIG /opt/goatd/config/goatd-config.yaml

ENTRYPOINT ["/bin/sh", "-c", "goatd ${CONFIG}"]