FROM redis:6

# Changes for openshift permissions
RUN chgrp -R 0 /data/ && \
    chmod -R g=u /data/
