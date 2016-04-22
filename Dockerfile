FROM alpine:3.3

# Add Code
ADD . /sc

# Install SmartContainers
RUN apk update && \
    apk add --no-cache python py-pip docker && \
    cd /sc && \
    python setup.py install && \
    rm -rf /sc

VOLUME /root/.sc
ENTRYPOINT ["sc"]
