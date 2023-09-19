FROM redis:6

# Changes for openshift permissions
RUN chgrp -R 0 /data/ && \
    chmod -R g=u /data/

RUN ls -l /

RUN chgrp -R 0 /data && \
    chmod -R g=u /data

RUN ls -l /

RUN chmod -R 777 /data

RUN ls -l /

RUN mkdir test123
