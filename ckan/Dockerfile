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

# Create user to arbitrary openshift uid/ gid:
RUN chmod -R 777 /etc
RUN chmod -R 777 /home
RUN mkdir /home/arbi
RUN chmod -R 777 /home/arbi
COPY setup/passwd /etc/passwd
RUN chmod 777 /etc/passwd

# Include adapted startup and prerun script
COPY setup/start_ckan_2.sh.override /srv/app/start_ckan.sh
RUN chmod 777 /srv/app/start_ckan.sh
COPY setup/prerun_2.py.override /srv/app/prerun.py
RUN chmod 777 /srv/app/prerun.py

# Adapt configparser and postgres checks
RUN sed -i "s|self.parser = ConfigParser()|self.parser = ConfigParser(interpolation=None)|g" /srv/app/src/ckan/ckan/cli/__init__.py
RUN sed -i "s|if not self._read_connection_has_correct_privileges():|#if not self._read_connection_has_correct_privileges():|g" /srv/app/src/ckan/ckanext/datastore/backend/postgres.py
RUN sed -i "s|self._log_or_raise('The read-only user has write privileges.')|#self._log_or_raise('The read-only user has write privileges.')|g" /srv/app/src/ckan/ckanext/datastore/backend/postgres.py

# Include gitconfig
COPY setup/.gitconfig /root/.gitconfig

# Install SSH and include SSH Config
RUN apk add --no-cache openssh
RUN mkdir /root/.ssh
COPY setup/ssh_config /root/.ssh/config
RUN echo -e ${CKANEXT_SECRET} > /root/.ssh/id_rsa
RUN ssh-keyscan -t rsa git.muenchen.de >> /root/.ssh/known_hosts
RUN chmod -R 755 /root/.ssh
RUN chmod 700 /root/.ssh
RUN chmod 400 /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/known_hosts

# Install ckanext-harvest
#RUN git clone -b lhm git@git.muenchen.de:lhm-udp-katalog-2/ckanext-harvest.git /srv/app/src/ckanext-harvest
#RUN pip3 install -e ${APP_DIR}/src/ckanext-harvest
#RUN pip3 install -e git+ssh://git@git.muenchen.de:lhm-udp-katalog-2/ckanext-harvest.git@lhm#egg=ckanext-harvest
#RUN pip3 install -r ${APP_DIR}/src/ckanext-harvest/pip-requirements.txt
RUN pip3 install -e 'git+ssh://git@git.muenchen.de:lhm-udp-katalog-2/ckanext-harvest.git@lhm#egg=ckanext-harvest' && \
    pip3 install -r ${APP_DIR}/src/ckanext-harvest/pip-requirements.txt

## Changes for openshift permissions: Allow all but /proc and /sys
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









