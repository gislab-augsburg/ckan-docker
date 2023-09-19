FROM redis:6

# Changes for openshift permissions
RUN mkdir /tmp/data
RUN chmod -R 777 /tmp/data
CMD redis-cli CONFIG SET dir /tmp/data
CMD redis-cli CONFIG SET dbfilename temp.rdb
CMD redis-cli BGSAVE


