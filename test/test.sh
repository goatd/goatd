#!/bin/bash

./goatd-start test/config.yaml &
goatd_pid=$!

sleep 1

kill $goatd_pid
