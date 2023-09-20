FROM redis:6

# Changes for openshift permissions
RUN mkdir /tmp/data
RUN chmod -R 777 /tmp/data
CMD ["redis-server;redis-cli CONFIG SET dir /tmp/data;redis-cli CONFIG SET dbfilename tdump.rdb;redis-cli BGSAVE"]

