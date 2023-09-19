FROM redis:6

# Changes for openshift permissions
RUN mkdir /tmp/data
RUN redis-cli CONFIG SET dir /tmp/data
RUN redis-cli CONFIG SET dbfilename temp.rdb
RUN redis-cli BGSAVE
RUN chmod -R 777 /tmp/data



