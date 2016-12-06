FROM keystone:newton

WORKDIR /root

ENV OS_USERNAME=admin \
    OS_PASSWORD=ADMIN_PASS \
    OS_PROJECT_NAME=admin \
    OS_USER_DOMAIN_NAME=default \
    OS_PROJECT_DOMAIN_NAME=default \
    OS_AUTH_URL=http://127.0.0.1:35357/v3 \
    OS_IDENTITY_API_VERSION=3

COPY supervisord.conf /etc/supervisord.conf

RUN echo "ServerName controller" >> /etc/apache2/apache2.conf \
    && mkdir -p /var/log/supervisor \
    && service mysql start \
    && service rabbitmq-server start \
    && service apache2 start \
    && openstack project create --domain default --description "Service Project" service \
    && openstack user create --domain default --password password devicedemo \
    && openstack role add --project service --user devicedemo admin \
    && openstack service create --name devicedemo --description "OpenStack Devicedemo" devicedemo \
    && openstack endpoint create --region RegionOne devicedemo public http://192.168.21.139:9511 \
    && openstack endpoint create --region RegionOne devicedemo internal http://192.168.21.139:9511 \
    && openstack endpoint create --region RegionOne devicedemo admin http://192.168.21.139:9511 \
    && apt-get install -y supervisor

EXPOSE 35357 5000

CMD ["/usr/bin/supervisord"]
