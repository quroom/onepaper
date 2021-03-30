#!/bin/bash
die(){
	local m="$1"  # the first arg
	local e=$2    # the second arg
	echo "$m"
	exit $e
}

ARG2=${2:--build}

# if not enough args displayed, display an error and die
[ $# -eq 0 ] && die "Usage: $0 [b|g] [--no-build]" 1

# Rest of script goes here
if [ $1 = "b" ]; then
    export Green=False
elif [ $1 = "g" ]; then
    unset Green
fi

if [ $ARG2 != "--no-build" ]; then
    cd frontend&&npm run build&&cd ..
fi
export DJANGO_DEBUG=False
export USE_S3=True
python manage.py collectstatic --no-input -i admin -i summernote -i debug_toolbar -i rest_framework -i MaterialIcons*
unset DJANGO_DEBUG
unset USE_S3