import ckan.plugins as p
from ckanext.spatial.interfaces import ISpatialHarvester
import os
from lxml import etree
import json
import ckanext.spatial.harvesters.base as base

class LHM_GP_Harvester(p.SingletonPlugin):

    p.implements(ISpatialHarvester, inherit=True)

    def get_package_dict(self, context, data_dict):

        print('--------------------MB_edit_10---plugin_get_package_dict_01')
        print(os.getcwd())
        print('-----------------------------------------------------------')

        package_dict = data_dict['package_dict']
        iso_values = data_dict['iso_values']
        xml_tree = data_dict['xml_tree']
        harvest_object = data_dict['harvest_object']

        '''
        # Check iso_values and package_dict before
        print('MB_edit_03__individual-name:')
        print(iso_values['responsible-organisation'][0]['individual-name'])
        print('MB_edit_03__update_frequ:')
        print(iso_values['frequency-of-update'])
        print('MB_edit_03__check_package_dict_before:')
        print(package_dict)
        print('-----------------------------------------')
        print(package_dict['extras'])
        '''

        # Write files for Schema Mapping I
        guid = iso_values['guid']
        path = f'/srv/app/data/{guid}'
        #os.mkdir(path)

        for key in package_dict:
            if type(package_dict[key]) == bytes:
                package_dict[key] = package_dict[key].decode('utf-8')
        data = json.dumps(package_dict, indent=4)
        f = open(f'{path}-package_dict_pre.json', 'w')
        f.write(data)
        f.close()

        # Check Harvest Source Configuration:
        # e.g.: {"default_extras": {"target_dataset_type":"isodata"}}
        # dataset type must be specified in active ckan schema
        for item in package_dict['extras']:
            if item['key'] == 'target_dataset_type':
                target_dataset_type = item['value']
                # Define target schema type:
                package_dict['type'] = target_dataset_type
                del package_dict['extras'][package_dict['extras'].index(item)]
            else:
                target_dataset_type = 'not_defined'


        # Map Iso Values to LHM-Iso-Schema
        if target_dataset_type == 'isodata':
            # Example hard-coded value:
            package_dict['harvest_source'] = 'Geoportal Muenchen'
            # Example iso_values nested:
            package_dict['author'] = iso_values['responsible-organisation'][0]['individual-name']
            package_dict['author_email'] = iso_values['responsible-organisation'][0]['contact-info']['email']
            # Example iso_values:
            package_dict['timeliness'] = iso_values['frequency-of-update']
            package_dict['metadata-standard-name'] = iso_values['metadata-standard-name']
            package_dict['metadata-standard-version'] = iso_values['metadata-standard-version']
            # Example package_dict extras:
            '''
            # Solution 1
            # if not schema dataset, name in extras must be different from schema field_name (= package_dict key):
            for item in package_dict['extras']:
                #if item['key'] == 'spatial-reference-system':
                    #package_dict['_spatial-reference-system'] = item['value']
            for item in package_dict['extras']:
                if item['key'] == 'spatial':
                    package_dict['_spatial'] = item['value']
            '''
            # Schema field name and extras field name cannot be the same,
            # raises Validation Error: {'Extras': 'There is a schema field with the same name'}.
            # Solution 2: Delete extras element after assigning as package-dict first level element,
            # get values from package_dict extras:
            for item in package_dict['extras']:
                if item['key'] == 'spatial-reference-system':
                    package_dict['spatial-reference-system'] = item['value']
                    i = package_dict['extras'].index(item)
                    del package_dict['extras'][i]
                elif item['key'] == 'spatial':
                    package_dict['spatial'] = item['value']
                    i = package_dict['extras'].index(item)
                    del package_dict['extras'][i]
                elif item['key'] == 'guid':
                    package_dict['guid'] = item['value']
                    i = package_dict['extras'].index(item)
                    del package_dict['extras'][i]
            
        # Map Iso Values to LHM-Schema
        # If not defined, target schema/ target_dataset type is "dataset"
        else:
            package_dict['author'] = iso_values['responsible-organisation'][0]['individual-name']
            package_dict['author_email'] = iso_values['responsible-organisation'][0]['contact-info']['email']
            package_dict['schema'] = 'baug'
            package_dict['ext_org'] = iso_values['responsible-organisation'][0]['organisation-name']
            package_dict['timeliness'] = 'auf_anforderung'
            package_dict['geometry_type'] = 'point'
            package_dict['archive'] = '{"archivability": "archivwuerdig", "justification": ""}'
            package_dict['intranet'] = '{"fachverfahren":"zugriffsuser", "geoinfoweb":"organisationseinheiten"}'
            package_dict['internet_publish'] = 'backend'
            package_dict['datenabgabe_extern_mit_auftrag'] = 'yes'
            package_dict['datenabgabe_extern'] = 'no'
            package_dict['open_data'] = 'all_open'
            # Example package_dict extras:
            # Schema field name and extras field name cannot be the same,
            # raises Validation Error: {'Extras': 'There is a schema field with the same name'}.
            # Solution 2: Delete extras element after assigning as package-dict first level element,
            # get values from iso_values:
            package_dict['spatial-reference-system'] = iso_values['spatial-reference-system']
            package_dict['guid'] = iso_values['guid']
            for item in package_dict['extras']:
                if item['key'] == 'spatial-reference-system':
                    del package_dict['extras'][package_dict['extras'].index(item)]
                elif item['key'] == 'guid':
                    del package_dict['extras'][package_dict['extras'].index(item)]
            

        # Mapping organisations
        #filepath = toolkit.config.get("ckanext.lhm.init_data", "schemas/init_group.json")
        #example implementation from ckanext-lhm, do similar for ckanext-iso
        filepath = '/srv/app/src/ckanext-iso/ckanext/iso/mapping_orgas.json'
        f = open(filepath)
        data = json.load(f)
        for orga, iso_orgas in data.items():
            if iso_values['responsible-organisation'][0]['individual-name'] in iso_orgas:
                package_dict['owner_org'] = orga
        
        '''
        # Check package_dict after
        print('MB_edit_04__check_package_dict_after:')
        print(package_dict)
        print('-----------------------------------------')
        print(package_dict['extras'])
        # Check xml_tree
        print('MB_edit_05__check_xml_tree:')
        print(xml_tree)
        '''

        # Write files for Schema Mapping II

        tree = etree.ElementTree(xml_tree)
        tree.write(f'{path}-iso_tree.xml')

        for key in iso_values:
            if type(iso_values[key]) == bytes:
                iso_values[key] = iso_values[key].decode('utf-8')
        data = json.dumps(iso_values, indent=4)
        f = open(f'{path}-iso_values.json', 'w')
        f.write(data)
        f.close()

        for key in package_dict:
            if type(package_dict[key]) == bytes:
                package_dict[key] = package_dict[key].decode('utf-8')
        data = json.dumps(package_dict, indent=4)
        f = open(f'{path}-package_dict_post.json', 'w')
        f.write(data)
        f.close()

        print('--------------------MB_edit_10---plugin_get_package_dict_02--status')
        status = _get_object_extra(harvest_object, 'status')
        #?? status = self.status = _get_object_extra(harvest_object, 'status')
        print(status)
        for item in package_dict['extras']:
            if item['key'] == 'force_import':
                if item['value'] == 'true':
                    if status == 'change':
                        base.SpatialHarvester.force_import = True
                    else:
                        base.SpatialHarvester.force_import = False

        #if status == 'change':
            #force_import = True
            #harvest_object.metadata_modified_date = '2030-01-01 00:00:00'
            
        
        #return package_dict, force_import
        return package_dict

##    def import_stage(self, context, data_dict):
##        
##        print('--------------------MB_edit_10---plugin_get_import_stage_01')
##
##        harvest_object = data_dict['harvest_object']
##        print(package_schema)
##
##        print('--------------------MB_edit_10---plugin_get_import_stage_02')

# Helper Functions

def _get_object_extra(harvest_object, key):
    '''
    Helper function for retrieving the value from a harvest object extra,
    given the key
    '''
    for extra in harvest_object.extras:
        if extra.key == key:
            return extra.value
    return None
        

