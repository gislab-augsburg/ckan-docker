FROM ckan/ckan-base:2.10.0
#FROM ckan/ckan-base:2.9.9

# Set up environment variables
ENV APP_DIR=/srv/app
ENV TZ=UTC
RUN echo ${TZ} > /etc/timezone

# Make sure both files are not exactly the same
RUN if ! [ /usr/share/zoneinfo/${TZ} -ef /etc/localtime ]; then \
        cp /usr/share/zoneinfo/${TZ} /etc/localtime ;\
    fi ;

# Changes for openshift permissions
#RUN chgrp -R 0 /srv/app && \
    #chmod -R g=u /srv/app

#RUN chgrp -R 0 /etc && \
    #chmod -R g=u /etc

#RUN chgrp -R 0 /usr/sbin && \
    #chmod -R g=u /usr/sbin

#RUN chgrp -R 0 /usr/sbin/uwsgi && \
    #chmod -R g=u /usr/sbin/uwsgi

#RUN chgrp -R 0 /tmp && \
    #chmod -R g=u /tmp

#RUN chmod 777 /srv/app
#RUN chmod 777 /tmp
#RUN chmod 777 /usr/sbin/uwsgi

#RUN chmod 777 /etc/uwsgi/uwsgi.ini
#RUN chmod 777 /srv/app/src/ckan/ckan-uwsgi.ini

#RUN apk add --no-cache su-exec

#RUN set -ex && apk --no-cache add sudo


#COPY setup/start_ckan_2.sh.override /srv/app/start_ckan.sh
#RUN chmod 775 /srv/app/start_ckan.sh

#USER ckan


#RUN sh /srv/app/start_ckan.sh


RUN chmod -R 777 /


