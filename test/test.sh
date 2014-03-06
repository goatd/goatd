#!/bin/bash

./goatd-start test/config.yaml &
goatd_pid=$!

sleep 1

echo
echo "        TESTING GET..."
echo

curl -v localhost:2222/heading && echo

curl localhost:2222/pony && echo

kill $goatd_pid
