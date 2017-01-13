====================================
Installing Devicedemo using DevStack
====================================

The ``devstack`` directory contains the files necessary to integrate Devicedemo with DevStack.

Configure DevStack to run Devicedemo

    $ DEVSTACK_DIR=/path/to/devstack


    $ cd ${DEVSTACK_DIR}
    $ cat >> local.conf << EOF
    [[local|localrc]]
    # devicedemo
    enable_plugin devicedemo https://github.com/yumaojun03/devicedemo.git master
    EOF

Run devstack as normal::

    $ ./stack.sh
