FROM ghcr.io/it-at-m/ckan-sddi-urban:udp-katalog-1.1.4-dev

USER root

# Set up environment variables
ENV APP_DIR=/srv/app
ENV TZ=UTC
RUN echo ${TZ} > /etc/timezone

# Make sure both files are not exactly the same
RUN if ! [ /usr/share/zoneinfo/${TZ} -ef /etc/localtime ]; then \
        cp /usr/share/zoneinfo/${TZ} /etc/localtime ;\
    fi ;

# Install wget for healthchecks
RUN set -ex && \
  apt update && apt install wget

# Install dev plugin
RUN set -ex && \
  pip3 install -e 'git+https://github.com/gislab-augsburg/ckanext-glab.git@0612d22#egg=ckanext-glab'

# Install iso plugin
RUN set -ex && \
  pip3 install -e 'git+https://github.com/gislab-augsburg/ckanext-iso.git@1cf93d0#egg=ckanext-iso'

# Set Plugins
ENV CKAN__PLUGINS "image_view text_view recline_view webpage_view \
    scheming_datasets scheming_groups scheming_organizations \
    spatial_metadata spatial_query spatial_harvest_metadata_api \
    composite hierarchy_display hierarchy_form lhm lhm_theme \
    resourcedictionary datastore xloader hierarchy_group_form \
    password_policy resource_proxy geo_view geojson_view wmts_view shp_view \
    harvest ckan_harvester csw_harvester waf_harvester doc_harvester \
    gdpr iso envvars"

# CKAN configuration
RUN set -ex && \
  ckan config-tool "${CKAN_INI}" "ckan.plugins = ${CKAN__PLUGINS}" && \
  ckan config-tool "${CKAN_INI}" "scheming.dataset_fallback = false" && \
  ckan config-tool "${CKAN_INI}" "scheming.presets = ckanext.scheming:presets.json ckanext.repeating:presets.json ckanext.composite:presets.json ckanext.lhm:schemas/presets.yaml" && \
  ckan config-tool "${CKAN_INI}" "scheming.dataset_schemas = ckanext.lhm:schemas/lhm_dataset.yaml ckanext.iso:lhm_isodata.yaml" && \
  ckan config-tool "${CKAN_INI}" "ckan.default.package_type = dataset" && \
# new  
  ckan config-tool "${CKAN_INI}" "ckan.spatial.validator.profiles = iso19139eden" && \
  ckan config-tool "${CKAN_INI}" "ckanext.spatial.harvest.continue_on_validation_errors = true" && \
  ckan config-tool "${CKAN_INI}" "ckan.locale_default = de" && \
# ckanext-iso
  ckan config-tool "${CKAN_INI}" "ckanext.iso.mapping_orgas = /srv/app/src/ckanext-iso/ckanext/iso/mapping_orgas.json"

# Install dev-requirements
RUN pip install -r /srv/app/src/ckan/dev-requirements.txt

USER ckan
