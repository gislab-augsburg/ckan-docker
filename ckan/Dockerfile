FROM ckan/ckan-base:ckan-2.10.0
#FROM ghcr.io/tum-gis/ckan-sddi-base:latest
#FROM ckan/ckan-base:dev-v2.10
#FROM martymcfly333/ckan-docker-edit-ini:latest
#FROM ghcr.io/tum-gis/ckan-sddi

# Set up environment variables
ENV APP_DIR=/srv/app
ENV TZ=UTC
RUN echo ${TZ} > /etc/timezone

# Make sure both files are not exactly the same
RUN if ! [ /usr/share/zoneinfo/${TZ} -ef /etc/localtime ]; then \
        cp /usr/share/zoneinfo/${TZ} /etc/localtime ;\
    fi ;

# Copy ckan.ini and images to container
COPY ckan.ini /srv/app/ckan.ini
COPY images/muc_2.png /srv/app/src/ckan/ckan/public/base/images/muc_2.png



# Install any extensions needed by your CKAN instance
# - Make sure to add the plugins to CKAN__PLUGINS in the .env file
# - Also make sure all extra configuration options are added to the CKAN config file (ckan.ini)
#   This can be done by creating an overriding start_ckan_dev_development.sh file:
#   (https://github.com/ckan/ckan-docker-base/blob/main/ckan-2.9/dev/setup/start_ckan_development.sh) ie: updating the 'ckan config-tool' lines
#   For more on config-tool please see https://docs.ckan.org/en/latest/maintaining/cli.html#config-tool-tool-for-editing-options-in-a-ckan-config-file
#   or using Crudini (https://github.com/pixelb/crudini) 
#
# For instance:
#
### XLoader ###
#RUN pip3 install -e 'git+https://github.com/ckan/ckanext-xloader.git@master#egg=ckanext-xloader' && \ 
#    pip3 install -r ${APP_DIR}/src/ckanext-xloader/requirements.txt && \
#    pip3 install -U requests[security]

### Harvester ###
RUN pip3 install -e 'git+https://github.com/ckan/ckanext-harvest.git@master#egg=ckanext-harvest' && \
    pip3 install -r ${APP_DIR}/src/ckanext-harvest/pip-requirements.txt
#!!!#Manual_or_startup##X## RUN ckan --config=/srv/app/ckan.ini harvester initdb
# will also require gather_consumer and fetch_consumer processes running (please see https://github.com/ckan/ckanext-harvest)

### Scheming ###
RUN  pip3 install -e 'git+https://github.com/ckan/ckanext-scheming.git@master#egg=ckanext-scheming'
RUN  pip3 install -e 'git+https://github.com/ckan/ckanext-scheming.git@master#egg=ckanext-scheming'
COPY extensions/camel_photos.yaml /srv/app/src/ckanext-scheming/ckanext/scheming/camel_photos.yaml
#COPY extensions/ckan_dataset.yaml /srv/app/src/ckanext-scheming/ckanext/scheming/ckan_dataset.yaml
COPY extensions/add_dataset.html /srv/app/src/ckan/ckan/templates/snippets/add_dataset.html

### Pages ###
#RUN  pip3 install -e git+https://github.com/ckan/ckanext-pages.git#egg=ckanext-pages

### DCAT ###
#RUN  pip3 install -e git+https://github.com/ckan/ckanext-dcat.git@v0.0.6#egg=ckanext-dcat && \
#     pip3 install -r https://raw.githubusercontent.com/ckan/ckanext-dcat/v0.0.6/requirements.txt

# Clone the extension(s) your are writing for your own project in the `src` folder
# to get them mounted in this image at runtime

# Apply any patches needed to CKAN core or any of the built extensions (not the
# runtime mounted ones)

### Spatial ###
#RUN apk add --no-cache python3-dev build-base gdal-dev
RUN pip install --upgrade pip
RUN pip install -e git+https://github.com/ckan/ckanext-spatial.git#egg=ckanext-spatial
RUN apk add geos-dev proj proj-util proj-dev
RUN export PROJ_DIR=/usr/bin
RUN PROJ_DIR=/usr/ pip install pyproj
#RUN pip install pyproj==2.6.1
#RUN pip3 install -e "git+https://github.com/ckan/ckanext-spatial.git#egg=ckanext-spatial"
#RUN apk add proj proj-util
COPY extensions/spatial/requirements.txt /srv/app/src/ckanext-spatial/requirements.txt
RUN pip3 install -r /srv/app/src/ckanext-spatial/requirements.txt
COPY extensions/spatial/search.html /srv/app/src/ckan/ckan/templates/package/search.html
COPY extensions/spatial/read.html /srv/app/src/ckan/ckan/templates/package/read.html
# Fix Harvesting Attribute Error 'str' and TypeError: str cannot be used as validator ... 
# in ckanext-spatial like in ckanext-harvest, see
# https://github.com/ckan/ckanext-harvest/pull/461/commits/e1b172490d44f203cd82aa616276a00f84a56fae :
COPY extensions/spatial/base.py /srv/app/src/ckanext-spatial/ckanext/spatial/harvesters/base.py
COPY extensions/spatial/license.py /srv/app/src/ckan/ckan/model/license.py
