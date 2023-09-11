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

#USER ckan

#RUN sh /srv/app/start_ckan.sh

#RUN chmod -R 777 /

# Create user to arbitrary openshift uid/ gid:
#RUN addgroup -g 1002890000 arbigroup
#RUN adduser --uid 1002890000 arbi arbigroup
RUN chmod -R 777 /etc
RUN chmod -R 777 /home
#RUN mkdir /home/arbi
#RUN chmod -R 777 /home/arbi
COPY setup/passwd /etc/passwd
RUN chmod 777 /etc/passwd

# Gitconfig
COPY setup/.gitconfig /root/.gitconfig

COPY setup/start_ckan_2.sh.override /srv/app/start_ckan.sh
RUN chmod 777 /srv/app/start_ckan.sh

COPY setup/prerun_2.py.override /srv/app/prerun.py
RUN chmod 777 /srv/app/prerun.py

RUN sed -i "s|self.parser = ConfigParser()|self.parser = ConfigParser(interpolation=None)|g" /srv/app/src/ckan/ckan/cli/__init__.py

RUN sed -i "s|if not self._read_connection_has_correct_privileges():|#if not self._read_connection_has_correct_privileges():|g" /srv/app/src/ckan/ckanext/datastore/backend/postgres.py
RUN sed -i "s|self._log_or_raise('The read-only user has write privileges.')|#self._log_or_raise('The read-only user has write privileges.')|g" /srv/app/src/ckan/ckanext/datastore/backend/postgres.py

RUN apk add --no-cache openssh

# SSH Config
RUN mkdir /root/.ssh
COPY setup/ssh_config /root/.ssh/config
RUN echo -e ${CKANEXT_SECRET} > /root/.ssh/id_rsa
COPY setup/known_hosts /root/.ssh/known_hosts

RUN chmod -R 755 /root/.ssh
RUN chmod 700 /root/.ssh
RUN chmod 400 /root/.ssh/id_rsa
#RUN chmod 777 /root/.ssh/config
RUN chmod 600 /root/.ssh/known_hosts

RUN ls -l -a /root/.ssh

RUN cat /root/.ssh/id_rsa
RUN cat /root/.ssh/config
RUN cat /root/.ssh/known_hosts

#RUN eval `ssh-agent`
#RUN ssh-add /root/.ssh/id_rsa

RUN git clone -b lhm git@git.muenchen.de:lhm-udp-katalog-2/ckanext-harvest.git /srv/app/src/ckanext-harvest
RUN pip3 install -e ${APP_DIR}/src/ckanext-harvest
#RUN pip3 install -e git+ssh://git@git.muenchen.de:lhm-udp-katalog-2/ckanext-harvest.git@lhm#egg=ckanext-harvest
RUN pip3 install -r ${APP_DIR}/src/ckanext-harvest/pip-requirements.txt


#RUN pip3 install -e 'git+ssh://git@git.muenchen.de:lhm-udp-katalog-2/ckanext-harvest.git@lhm#egg=ckanext-harvest' && \
    #pip3 install -r ${APP_DIR}/src/ckanext-harvest/pip-requirements.txt

## Allow all but /proc and /sys

RUN chmod -R 777 /bin
RUN chmod -R 777 /dev 
RUN chmod -R 777 /docker-entrypoint.d
#RUN chmod -R 777 /etc
#RUN chmod -R 777 /home 
RUN chmod -R 777 /lib 
RUN chmod -R 777 /media
RUN chmod -R 777 /mnt
RUN chmod -R 777 /opt
RUN chmod -R 777 /root
RUN chmod -R 777 /run
RUN chmod -R 777 /sbin
RUN chmod -R 777 /srv
RUN chmod -R 777 /tmp
RUN chmod -R 777 /usr
RUN chmod -R 777 /var









