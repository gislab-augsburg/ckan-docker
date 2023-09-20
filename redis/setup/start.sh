#!/bin/bash

redis-server
redis-cli CONFIG SET dir /tmp/data
redis-cli CONFIG SET dbfilename tdump.rdb
redis-cli BGSAVE
