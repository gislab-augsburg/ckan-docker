FROM redis:6

# Changes for openshift permissions
RUN chgrp -R 0 /data/ && \
    chmod -R g=u /data/

RUN ls -l /data

RUN chgrp -R 0 /data && \
    chmod -R g=u /data

RUN ls -l /data

RUN chmod -R 777 /data

RUN ls -l /data

RUN mkdir test123
