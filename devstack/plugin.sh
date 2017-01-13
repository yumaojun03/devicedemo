# Devicedemo devstack plugin
# Install and start **Devicedemo** service
# To enable a minimal set of Devicedemo services:
# - add the following to the [[local|localrc]] section in the local.conf file:
#   # enable Devicedemo
#   enable_plugin devicedemo https://github.com/yumaojun03/devicedemo.git
#   enable_service devicedemo-api
#
# stack.sh
# ---------
# install_devicedemo
# install_python_devicedemoclient
# configure_devicedemo
# init_devicedemo
# start_devicedemo
# stop_devicedemo
# cleanup_devicedemo


# Save trace setting
XTRACE=$(set +o | grep xtrace)
set +o xtrace


# Support potential entry-points console scripts in VENV or not
if [[ ${USE_VENV} = True ]]; then
    PROJECT_VENV["devicedemo"]=${DEVICEDEMO_DIR}.venv
    DEVICEDEMO_BIN_DIR=${PROJECT_VENV["devicedemo"]}/bin
else
    DEVICEDEMO_BIN_DIR=$(get_python_exec_prefix)
fi


# Functions
# ---------

# Activities to do before devicedemo has been installed.
function preinstall_devicedemo {
    echo_summary "Preinstall not in virtualenv context. Skipping."
}

# # install_python_devicedemoclient() - Collect source and prepare
# function install_python_devicedemoclient {
#     # Install from git since we don't have a release (yet)
#     echo_summary "Install Devicedemo Client"
#     git_clone_by_name "python-devicedemoclient"
#     setup_dev_lib "python-devicedemoclient"
# }

# install_devicedemo() - Collect source and prepare
function install_devicedemo {
    # install_python_devicedemoclient
    setup_develop $DEVICEDEMO_DIR
    sudo install -d -o $STACK_USER -m 755 $DEVICEDEMO_CONF_DIR
}

# configure_devicedemo() - Set config files, create data dirs, etc
function configure_devicedemo {
    cp $DEVICEDEMO_DIR$DEVICEDEMO_CONF_DIR/policy.json $DEVICEDEMO_CONF_DIR
    cp $DEVICEDEMO_DIR$DEVICEDEMO_CONF_DIR/api_paste.ini $DEVICEDEMO_CONF_DIR

    # default
    iniset_rpc_backend devicedemo $DEVICEDEMO_CONF DEFAULT
    iniset $DEVICEDEMO_CONF DEFAULT notification_topics 'notifications'
    iniset $DEVICEDEMO_CONF DEFAULT debug "$ENABLE_DEBUG_LOG_LEVEL"

    # database
    iniset $DEVICEDEMO_CONF database connection `database_connection_url devicedemo`

    # keystone middleware
    configure_auth_token_middleware $DEVICEDEMO_CONF devicedemo $DEVICEDEMO_AUTH_CACHE_DIR
}

# Create devicedemo related accounts in Keystone
function create_devicedemo_accounts {
    if is_service_enabled devicedemo-api; then

        create_service_user "devicedemo" "admin"

        local devicedemo_service=$(get_or_create_service "devicedemo" \
            "device" "OpenStack Device Service")

        get_or_create_endpoint $devicedemo_service \
            "$REGION_NAME" \
            "$DEVICEDEMO_SERVICE_PROTOCOL://$DEVICEDEMO_SERVICE_HOST:$DEVICEDEMO_SERVICE_PORT/" \
            "$DEVICEDEMO_SERVICE_PROTOCOL://$DEVICEDEMO_SERVICE_HOST:$DEVICEDEMO_SERVICE_PORT/" \
            "$DEVICEDEMO_SERVICE_PROTOCOL://$DEVICEDEMO_SERVICE_HOST:$DEVICEDEMO_SERVICE_PORT/"
    fi

    # Make devicedemo an admin
    get_or_add_user_project_role admin devicedemo service
}

# create_devicedemo_cache_dir() - Part of the init_devicedemo() process
function create_devicedemo_cache_dir {
    # Create cache dir
    sudo install -d -o $STACK_USER $DEVICEDEMO_AUTH_CACHE_DIR
    sudo install -d -o $STACK_USER $DEVICEDEMO_AUTH_CACHE_DIR/api
    sudo install -d -o $STACK_USER $DEVICEDEMO_AUTH_CACHE_DIR/registry
}

# create_devicedemo_data_dir() - Part of the init_devicedemo() process
function create_devicedemo_data_dir {
    # Create data dir
    sudo install -d -o $STACK_USER $DEVICEDEMO_DATA_DIR
    sudo install -d -o $STACK_USER $DEVICEDEMO_DATA_DIR/locks
}

# init_devicedemo() - Initialize Devicedemo database
function init_devicedemo {
    create_devicedemo_cache_dir
    create_devicedemo_data_dir

    # (Re)create devicedemo database
    recreate_database devicedemo utf8

    # Migrate devicedemo database
    $DEVICEDEMO_BIN_DIR/devicedemo-dbmanage upgrade
}

# start_devicedemo() - Start running processes, including screen
function start_devicedemo {
    run_process devicedemo-api "$DEVICEDEMO_BIN_DIR/devicedemo-api --config-file $DEVICEDEMO_CONF"

    echo "Waiting for devicedemo-api ($DEVICEDEMO_SERVICE_HOST:$DEVICEDEMO_SERVICE_PORT) to start..."
    if ! timeout $SERVICE_TIMEOUT sh -c "while ! wget --no-proxy -q -O- http://$DEVICEDEMO_SERVICE_HOST:$DEVICEDEMO_SERVICE_PORT; do sleep 1; done"; then
        die $LINENO "devicedemo-api did not start"
    fi
}

# stop_devicedemo() - Stop running processes
function stop_devicedemo {
    # Kill the devicedemo screen windows
    for serv in devicedemo-api; do
        stop_process $serv
    done
}

# cleanup_devicedemo() - Remove residual data files, anything left over from previous
# runs that a clean run would need to clean up
function cleanup_devicedemo {
    # Clean up dirs
    sudo rm -rf $DEVICEDEMO_AUTH_CACHE_DIR
    sudo rm -rf $DEVICEDEMO_CONF_DIR
    sudo rm -rf $DEVICEDEMO_OUTPUT_BASEPATH
    sudo rm -rf $DEVICEDEMO_DATA_DIR
}

# This is the main for plugin.sh
if is_service_enabled devicedemo-api; then
    if [[ "$1" == "stack" && "$2" == "pre-install" ]]; then
        # Set up system services
        echo_summary "Configuring system services for Devicedemo"
        preinstall_devicedemo

    elif [[ "$1" == "stack" && "$2" == "install" ]]; then
        echo_summary "Installing Devicedemo"
        # Use stack_install_service here to account for vitualenv
        stack_install_service devicedemo

    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        echo_summary "Configuring Devicedemo"
        configure_devicedemo
        # Get devicedemo keystone settings in place
        create_devicedemo_accounts

    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        # Initialize devicedemo
        echo_summary "Initializing Devicedemo"
        init_devicedemo

        # Start the Devicedemo API and Devicedemo processor components
        echo_summary "Starting Devicedemo"
        start_devicedemo
    fi

    if [[ "$1" == "unstack" ]]; then
        echo_summary "Shutting Down Devicedemo"
        stop_devicedemo
    fi

    if [[ "$1" == "clean" ]]; then
        echo_summary "Cleaning Devicedemo"
        cleanup_devicedemo
    fi
fi


# Restore xtrace
$XTRACE

