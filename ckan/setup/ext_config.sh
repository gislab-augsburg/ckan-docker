echo Configuring ckan extensions
# ckanext-scheming config
#ckan config-tool ${APP_DIR}/ckan.ini scheming.dataset_schemas='ckanext.scheming:ckan_dataset.yaml ckanext.scheming:camel_photo.yaml ckanext.scheming:ckan_formpages.yaml'
#ckan config-tool ${APP_DIR}/ckan.ini ckan.default.package_type=camel-photo
#ckan config-tool ${APP_DIR}/ckan.ini ckanext.xloader.api_token=abcde
#ckan config-tool ${APP_DIR}/ckan.ini scheming.presets='ckanext.scheming:presets.json ckanext.repeating:presets.json ckanext.composite:presets.json'
#ckan config-tool ${APP_DIR}/ckan.ini scheming.dataset_schemas=ckanext.lhm:lhm_dataset.yaml
ckan config-tool ${APP_DIR}/ckan.ini ckan.default.package_type=dataset
