echo Configuring ckan extensions
# ckanext-scheming config
ckan config-tool ${APP_DIR}/ckan.ini scheming.dataset_schemas=ckanext.scheming:camel_photos.yaml
ckan config-tool ${APP_DIR}/ckan.ini ckan.default.package_type=camel-photos