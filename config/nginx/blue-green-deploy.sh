#!/bin/bash
die(){
	local m="$1"  # the first arg 
	local e=$2    # the second arg
	echo "$m" 
	exit $e
}

# if not enough args displayed, display an error and die
[ $# -eq 0 ] && die "Usage: $0 [b|g]" 1

# Rest of script goes here
if [ $1 = "b" ]; then
    sudo ln -sf /home/ubuntu/onepaper/config/nginx/nginx-config /etc/nginx/sites-available/default
    echo "To Blue"
    ls -al /etc/nginx/sites-available/default
elif [ $1 = "g" ]; then
    echo "To Green"
    sudo ln -sf /home/ubuntu/onepaper/config/nginx/green-nginx-config /etc/nginx/sites-available/default
    ls -al /etc/nginx/sites-available/default
else
    echo "argument can be [b|g]"
fi

