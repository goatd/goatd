#!/bin/bash

function log() {
    echo ""
    echo "        $1"
    echo
}

./goatd-start test/config.yaml &
goatd_pid=$!

sleep 2

log "STARTED GOATD WITH PID=$goatd_pid"
log "TESTING GET..."

curl -i localhost:2222/heading && echo

curl -i localhost:2222/pony && echo

log "TESTING POST..."

curl -i -X POST -H "Content-Type: application/json" -d '{"quit": true}' http://localhost:2222
echo

sleep 2

if kill $goatd_pid 2> /dev/null; then
    log "FAILED TO STOP, KILLED GOATD";
else
    log "TESTS FINISHED";
fi
