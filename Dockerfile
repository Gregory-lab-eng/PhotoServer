FROM ubuntu:latest
LABEL authors="Gregory Strakhov"

ENTRYPOINT ["top", "-b"]