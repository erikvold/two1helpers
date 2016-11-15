#!/bin/bash
# usage ./portkiller.sh $1
PORT_NUMBER=$1
echo "searching for processes listening on $PORT_NUMBER which are"
lsof -i tcp:${PORT_NUMBER} | xargs -d\n
read -r -p "Are you sure you want to kill these? [y/N] " response
case $response in
    [yY][eE][sS]|[yY])
        lsof +c14 -i tcp:${PORT_NUMBER} | awk 'NR!=1 {print $2}' | xargs kill
        ;;
    *)
        echo "ok, never mind!"
        ;;
esac
