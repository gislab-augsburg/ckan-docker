FROM redis:6

# Changes for openshift permissions
RUN mkdir /tmp/data
RUN chmod -R 777 /tmp/data
ADD setup/start.sh /tmp/
RUN chmod +x /tmp/start.sh
CMD ["/tmp/start.sh"]
