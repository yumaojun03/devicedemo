FROM ubuntu:16.04

RUN apt install software-properties-common \
    && add-apt-repository cloud-archive:newton \
    && apt update && apt dist-upgrade \
    && apt install python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev zlib1g-dev git tmux lrzsz vim python-pip python-tox uwsgi \
    && apt-get install apache2 libapache2-mod-wsgi \
    && a2enmod wsgi \
    && apt install python-openstackclient \
    &&