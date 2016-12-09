### 基于单个docker部署和运行Keystone服务

  这里将Keystone打包成一个独立个镜像，然后基于该镜像可以build出我们需要的
  keystone服务

- 获取keystone的获取镜像

    可能的问题
    
    > 可能会出现无法push/pull镜像到私有仓库的问题。这是因为我们启动的registry服务不是安全可信赖的。这是我们需要修改docker的配置文件/etc/default/docker，添加下面的内容，
    DOCKER_OPTS="--insecure-registry xxx.xxx.xxx.xxx:5000"
    然后重启docker后台进程，
    $ sudo service docker restart
    这是再push/pull即可。
    

- 创建合适的Keystone服务

  + 修改Dockerfile（devicedemo/Deploy/huge_docker/keystone/Dockerfile)中FROM部分为你 当前镜像
    
  > 比如你获取的镜像为： 192.168.1.105:5000/keystone:newton, Dockefile中FROM哪行就需要修改成
  FROM 192.168.1.105:5000/keystone:newton
  
  + 修改devicedemo服务地址
    
  > Keystone的build的过程中会注册devicedemo到keystone服务里面，
   因此这里你需要手动修改 devicedemo的服务地址，与你本地的服务对应,
   比如 替换 Dockefile中 192.168.21.139:9511 为你devicedemo真正的地址。
    
  + build Keystone服务镜像
  
  > 进入到build keystone 的目录： devicedemo/Deploy/huge_docker/keystone
    
```
maojun@maojun-mbp# pwd
/Users/maojun/PycharmProjects/devicedemo/Deploy/huge_docker/keystone
maojun@maojun-mbp# docker build -t keystone:newton_devicedemo .
Sending build context to Docker daemon  5.12 kB
Step 1 : FROM keystone:newton
 ---> 6ef614e0ce71
Step 2 : WORKDIR /root
 ---> Running in 14b8fd7fee3d
 ---> 65e6a1e40078
Removing intermediate container 14b8fd7fee3d
Step 3 : ENV OS_USERNAME admin OS_PASSWORD ADMIN_PASS OS_PROJECT_NAME admin OS_USER_DOMAIN_NAME default OS_PROJECT_DOMAIN_NAME default OS_AUTH_URL http://127.0.0.1:35357/v3 OS_IDENTITY_API_VERSION 3
 ---> Running in 86aebba59590
 ---> b075121bf881
Removing intermediate container 86aebba59590
Step 4 : COPY supervisord.conf /etc/supervisord.conf
 ---> 4ccf1b52b31c
Removing intermediate container fc597f6ad1a8
Step 5 : RUN echo "ServerName controller" >> /etc/apache2/apache2.conf     && mkdir -p /var/log/supervisor     && service mysql start     && service rabbitmq-server start     && service apache2 start     && openstack project create --domain default --description "Service Project" service     && openstack user create --domain default --password password devicedemo     && openstack role add --project service --user devicedemo admin     && openstack service create --name devicedemo --description "OpenStack Devicedemo" devicedemo     && openstack endpoint create --region RegionOne devicedemo public http://192.168.21.139:9511     && openstack endpoint create --region RegionOne devicedemo internal http://192.168.21.139:9511     && openstack endpoint create --region RegionOne devicedemo admin http://192.168.21.139:9511     && apt-get install -y supervisor
 ---> Running in 15a92cf50487
 * Starting MariaDB database server mysqld
   ...done.
 * Starting RabbitMQ Messaging Server rabbitmq-server
   ...done.
 * Starting Apache httpd web server apache2
 *
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | Service Project                  |
| domain_id   | default                          |
| enabled     | True                             |
| id          | fce6c331fd3b46ff9f9f38988d334882 |
| is_domain   | False                            |
| name        | service                          |
| parent_id   | default                          |
+-------------+----------------------------------+
+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| domain_id           | default                          |
| enabled             | True                             |
| id                  | 69e08609ba4546a59438dadc77ec0934 |
| name                | devicedemo                       |
| password_expires_at | None                             |
+---------------------+----------------------------------+
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | OpenStack Devicedemo             |
| enabled     | True                             |
| id          | 6bb07002037041a7a718d7124ebb9080 |
| name        | devicedemo                       |
| type        | devicedemo                       |
+-------------+----------------------------------+
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | c511da43c4e8434e95fda2b0664bedf7 |
| interface    | public                           |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 6bb07002037041a7a718d7124ebb9080 |
| service_name | devicedemo                       |
| service_type | devicedemo                       |
| url          | http://192.168.21.139:9511       |
+--------------+----------------------------------+
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | ed2a17b4244945e8ae7076bc994161fd |
| interface    | internal                         |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 6bb07002037041a7a718d7124ebb9080 |
| service_name | devicedemo                       |
| service_type | devicedemo                       |
| url          | http://192.168.21.139:9511       |
+--------------+----------------------------------+
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 1d586d996255427392996887db742cc9 |
| interface    | admin                            |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 6bb07002037041a7a718d7124ebb9080 |
| service_name | devicedemo                       |
| service_type | devicedemo                       |
| url          | http://192.168.21.139:9511       |
+--------------+----------------------------------+
Reading package lists...
Building dependency tree...
Reading state information...
The following additional packages will be installed:
  python-meld3
Suggested packages:
  supervisor-doc
The following NEW packages will be installed:
  python-meld3 supervisor
0 upgraded, 2 newly installed, 0 to remove and 0 not upgraded.
Need to get 283 kB of archives.
After this operation, 1549 kB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu xenial/universe amd64 python-meld3 all 1.0.2-2 [30.9 kB]
Get:2 http://archive.ubuntu.com/ubuntu xenial/universe amd64 supervisor all 3.2.0-2 [252 kB]
debconf: unable to initialize frontend: Dialog
debconf: (TERM is not set, so the dialog frontend is not usable.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype
dpkg-preconfigure: unable to re-open stdin:
Fetched 283 kB in 13s (21.1 kB/s)
Selecting previously unselected package python-meld3.
(Reading database ... 27950 files and directories currently installed.)
Preparing to unpack .../python-meld3_1.0.2-2_all.deb ...
Unpacking python-meld3 (1.0.2-2) ...
Selecting previously unselected package supervisor.
Preparing to unpack .../supervisor_3.2.0-2_all.deb ...
Unpacking supervisor (3.2.0-2) ...
Processing triggers for systemd (229-4ubuntu12) ...
Setting up python-meld3 (1.0.2-2) ...
Setting up supervisor (3.2.0-2) ...
invoke-rc.d: could not determine current runlevel
invoke-rc.d: policy-rc.d denied execution of start.
Processing triggers for systemd (229-4ubuntu12) ...
 ---> c401f00d4049
Removing intermediate container 15a92cf50487
Step 6 : EXPOSE 35357 5000
 ---> Running in ecab5df6dd48
 ---> 8202ac4ea25b
Removing intermediate container ecab5df6dd48
Step 7 : CMD /usr/bin/supervisord
 ---> Running in f871aff12a55
 ---> bd1bea7a3d34
Removing intermediate container f871aff12a55
Successfully built bd1bea7a3d34

```

### devicedemo服务的启动

  这部分和 源码安装相同