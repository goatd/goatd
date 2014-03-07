#!/bin/bash

END="\e[0m"
RED="\e[1;31m"
GREEN="\e[1;32m"
BLUE="\e[1;34m"

function log() {
    echo  -e "    $1"
}

function test() {
    cmd=$1

    log " testing$BLUE $cmd\n$END"
    eval "$cmd"
    if $? 2> /dev/null; then
        log $RED"FAILED"$END
    else
        log $GREEN"PASSED"$END
    fi
    echo
}

./goatd-start test/config.yaml &
goatd_pid=$!

sleep 2

log "STARTED GOATD WITH PID=$goatd_pid"

log "TESTING POST..."

test "curl -i localhost:2222/heading"
test "curl -i localhost:2222/pony"

test "curl -i -X POST -H \"Content-Type: application/json\" -d '{\"quit\": true}' http://localhost:2222"
echo

sleep 2

if kill $goatd_pid 2> /dev/null; then
    log "FAILED TO STOP, KILLED GOATD";
else
    log "TESTS FINISHED";
fi
