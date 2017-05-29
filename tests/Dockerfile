FROM themattrix/tox-base
WORKDIR /app
ADD . /app
ONBUILD RUN bash -c "TOXBUILD=true tox"
CMD ["tox"]
