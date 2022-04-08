#!/bin/sh

cd src
celery -A celery_tasks worker -l info