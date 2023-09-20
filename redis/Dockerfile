FROM redis:6

# Changes for openshift permissions
RUN mkdir /tmp/data
RUN chmod -R 777 /tmp/data
COPY setup/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod 775 /usr/local/bin/docker-entrypoint.sh

