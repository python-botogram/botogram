# Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
# Documentation released under the MIT license (see LICENSE)

# Image to build doc
FROM python:3.6-alpine3.6 as BUILDER
RUN apk update \
    && apk add git bash make
RUN pip install invoke virtualenv
COPY ./requirements-docs.txt /requirements-docs.txt
RUN pip install  -r /requirements-docs.txt
COPY ./  /botogram
RUN cd /botogram && invoke docs && cd .netlify && make 

# Image final
FROM nginx:latest
RUN rm /etc/nginx/conf.d/default.conf
COPY /nginx-doc.conf  /etc/nginx/conf.d/default.conf
COPY --from=BUILDER /botogram/.netlify/build/ ./botogram
ARG botogram_version=dev
ENV env_botogram_version=$botogram_version
RUN sed 's/RELEASE/'"$env_botogram_version"'/g' -i /etc/nginx/conf.d/default.conf
