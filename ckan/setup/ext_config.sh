echo Configuring ckan extensions
# ckanext-scheming config
ckan config-tool ${APP_DIR}/ckan.ini scheming.dataset_schemas='ckanext.scheming:camel_photo.yaml ckanext.scheming:ckan_formpages.yaml'
#ckan config-tool ${APP_DIR}/ckan.ini ckan.default.package_type=camel-photo
ckan config-tool ${APP_DIR}/ckan.ini ckanext.xloader.api_token = abc