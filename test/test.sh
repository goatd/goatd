#!/bin/bash

./goatd-start test/config.yaml &
goatd_pid=$!

sleep 1

echo
echo "        TESTING GET..."
echo

curl -i localhost:2222/heading && echo

curl -i localhost:2222/pony && echo

echo
echo "        TESTING POST..."
echo

curl -i -X POST -H "Content-Type: application/json" -d '{"quit": true}' http://localhost:2222

echo kill $goatd_pid
