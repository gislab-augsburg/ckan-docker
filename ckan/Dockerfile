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

##gitconfig, ssh

# Install ckanext-xLoader
RUN git clone -b lhm git@git.muenchen.de:lhm-udp-katalog-2/ckanext-xloader.git ${APP_DIR}/src/ckanext-xloader
RUN pip3 install -e ${APP_DIR}/src/ckanext-xloader && \ 
    pip3 install -r ${APP_DIR}/src/ckanext-xloader/requirements.txt && \
    pip3 install -U requests[security]

# Install ckanext-harvest
RUN git clone -b lhm git@git.muenchen.de:lhm-udp-katalog-2/ckanext-harvest.git ${APP_DIR}/src/ckanext-harvest
RUN pip3 install -e ${APP_DIR}/src/ckanext-harvest
RUN pip3 install -r ${APP_DIR}/src/ckanext-harvest/pip-requirements.txt

# Install ckanext-scheming
RUN git clone -b lhm git@git.muenchen.de:lhm-udp-katalog-2/ckanext-scheming.git ${APP_DIR}/src/ckanext-scheming
RUN pip3 install -e ${APP_DIR}/src/ckanext-scheming

# Install ckanext-spatial
RUN pip install --upgrade pip
RUN git clone -b lhm git@git.muenchen.de:lhm-udp-katalog-2/ckanext-spatial.git ${APP_DIR}/src/ckanext-spatial
RUN pip install -e ${APP_DIR}/src/ckanext-spatial
RUN apk add geos-dev proj proj-util proj-dev
RUN export PROJ_DIR=/usr/bin
# Until pyproj 3.6.0 uncompatibility with Cython 3.0 is solved (https://github.com/pyproj4/pyproj/issues/1342, https://bugs.gentoo.org/911736):
RUN git clone https://github.com/pyproj4/pyproj.git ${APP_DIR}/src/pyproj
RUN PROJ_DIR=/usr/ pip install -e ${APP_DIR}/src/pyproj
RUN pip install Shapely==1.8.5
RUN pip3 install -r ${APP_DIR}/src/ckanext-spatial/requirements.txt
COPY extensions/spatial/search.html ${APP_DIR}/src/ckan/ckan/templates/package/search.html
COPY extensions/spatial/read.html ${APP_DIR}/src/ckan/ckan/templates/package/read.html
# Fix Harvesting Attribute Error 'str' and TypeError: str cannot be used as validator ... 
# in ckanext-spatial like in ckanext-harvest, see 
# https://github.com/ckan/ckanext-harvest/pull/461/commits/e1b172490d44f203cd82aa616276a00f84a56fae :
# COPY extensions/spatial/base.py /srv/app/src/ckanext-spatial/ckanext/spatial/harvesters/base.py -> changed in ckanext-spatial
COPY extensions/spatial/license.py /srv/app/src/ckan/ckan/model/license.py

# Copy docker-entrypoint scripts
COPY setup/ext_config.sh /docker-entrypoint.d/ext_config.sh

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







