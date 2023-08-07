FROM ubuntu:22.04

LABEL maintainer="Fernando Cruz"

ARG GROUPID
ARG USERID
ARG NODE_VERSION=18
ARG POSTGRES_VERSION=15

WORKDIR /code

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=UTC

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
    && apt-get install -y gnupg gosu software-properties-common curl ca-certificates \
    zip unzip git supervisor sqlite3 libcap2-bin libpng-dev python2 dnsutils librsvg2-bin \
    build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev \
    libffi-dev libsqlite3-dev wget libbz2-dev pkg-config \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get install -y python3 python3-pip python3.11 python3.11-dev python3.11-venv \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 \
    # && pip3.11 install virtualenv \
    && apt-get update \
    && curl -sLS https://deb.nodesource.com/setup_$NODE_VERSION.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm \
    && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | tee /etc/apt/keyrings/yarn.gpg >/dev/null \
    && echo "deb [signed-by=/etc/apt/keyrings/yarn.gpg] https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list \
    && curl -sS https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | tee /etc/apt/keyrings/pgdg.gpg >/dev/null \
    && echo "deb [signed-by=/etc/apt/keyrings/pgdg.gpg] http://apt.postgresql.org/pub/repos/apt jammy-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && apt-get update \
    && apt-get install -y yarn \
    && apt-get install -y mysql-client \
    && apt-get install -y postgresql-client-$POSTGRES_VERSION \
    && apt-get -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN groupadd --force -g $GROUPID fly
RUN useradd -ms /bin/bash --no-user-group -g $GROUPID -u $USERID fly

COPY requirements_common.txt /code
COPY requirements.txt /code

COPY start-container /usr/local/bin/start-container
COPY wait-for-it.sh /
COPY entry_point.sh /
COPY entry_point_node.sh /
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN chmod +x /usr/local/bin/start-container

USER fly
# RUN pip3.11 install --no-cache-dir -r /code/requirements.txt

EXPOSE 8000

ENTRYPOINT ["start-container"]
