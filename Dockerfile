FROM harrisbaird/scrapyd:py2

ENV BUILD_PACKAGES=build-base \
    RUNTIME_PACKAGES="libssl1.0 supervisor"

WORKDIR /app

ADD requirements.txt /app

RUN apk --update add $RUNTIME_PACKAGES && \
  apk add --virtual build-dependencies $BUILD_PACKAGES && \
  pip uninstall -y scrapyd && \
  pip --no-cache-dir install -r requirements.txt && \
  apk del build-dependencies && \
  rm -rf /var/cache/apk/*

ADD . /app

# Build the project and deploy it to scrapyd.
RUN scrapyd & PID=$! && \
   sleep 5 && \
   scrapyd-deploy && \
   kill $PID

EXPOSE 6800 6900

ENTRYPOINT ["supervisord", "-c", "supervisord.conf"]
