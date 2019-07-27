#!/bin/bash
# -*- coding: utf-8 -*-

# Set-up important variables

PROJECT_DIR="$( dirname $0 )"/..
PACKAGE_DIR=$PROJECT_DIR/package
RELEASE_ENV=$PROJECT_DIR/release_env
RELEASE_ENV_REQS=$PROJECT_DIR/requirements-release.txt


activate_release_env() {
    if [ ! -d $RELEASE_ENV ]; then
        echo "Creating a virtual env." && python -m venv $RELEASE_ENV
    fi
    source $RELEASE_ENV/bin/activate
    pip install -r $RELEASE_ENV_REQS
}

deactivate_release_env() {
    deactivate
}
