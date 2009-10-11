#!/bin/bash

APPENGINE_DIRECTORY=/mnt/home/google_appengine

export PYTHONPATH=$PYTHONPATH:$APPENGINE_DIRECTORY:$APPENGINE_DIRECTORY/lib/yaml/lib:$APPENGINE_DIRECTORY/lib/webob:$APPENGINE_DIRECTORY/lib/django

/usr/bin/nosetests 
