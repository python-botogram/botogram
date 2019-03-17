# Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
# Documentation released under the MIT license (see LICENSE)

# image to build doc
FROM python:3.6-alpine3.6 as BUILDER
RUN apk update \
    && apk add git bash make 
RUN pip install invoke virtualenv
COPY ./requirements-docs.txt /requirements-docs.txt
RUN pip install  -r /requirements-docs.txt
COPY ./  /botogram
RUN cd /botogram && invoke docs && cd .netlify && make 

RUN apk add tree
RUN tree /botogram/.netlify/build

# image final
FROM nginx:latest
ENV botogram_version dev
RUN rm /etc/nginx/conf.d/default.conf
ADD https://gist.githubusercontent.com/matteb99/4ab0dffc07558273401220f3e0426f5a/raw/7fc18180327f57b6ab8bbbad9f629a0e5955a4a1/gistfile1.txt  /etc/nginx/conf.d/default.conf
RUN sed 's/RELEASE/'"$botogram_version"'/g' -i /etc/nginx/conf.d/default.conf 
COPY --from=BUILDER /botogram/.netlify/build/ ./botogram 
