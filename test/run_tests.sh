#!/bin/bash

./goatd-start &
goatd_pid=$!

echo "goatd started"

sleep 1

kill $goatd_pid
