## Translate ckan-docker to openshift input yaml files for LHM CAP with kompose and adaptations
## Needs docker-compose and kompose to be installed
## Import the resulting capfiles to openshift with 'oc create -f ..'
## For that, be sure to be logged into openshift and right project, check with "oc projects"

import os
import shutil
import time

## Define repo and branch with dockerfiles used for buildconfigs and source secret used for acces to repo/ host key verification during builds.
## If no key verification needed, change source_secret value to ''
## Define openshift project for adaptation of ckan route:
repo = 'git@git.muenchen.de:lhm-udp-katalog-2/ckan-docker-ga.git'
branch = 'openshift'
source_secret = 'gitlab-source-secret-ckan-ga'
openshift_project = 'udpkatalog-dev'

# Define lines for insertion of repo, branch and source secret
repo_line = 'uri: ' + repo
branch_line = 'ref: ' + branch
if source_secret != '':
    source_secret_lines = 'source:\n    sourceSecret:\n      name: ' + source_secret
else:
    source_secret_lines = 'source:'

# Get .env values as dict
env_vars = {}
with open('.env') as f:
    for line in f:
        if line.startswith('#') or not line.strip():
            continue
        # if 'export' not in line:
        #     continue
        key, value = line.strip().split('=', 1)
        # os.environ[key] = value  # Load to local environ
        env_vars[key] = value

# Construct secondary secret environment variables
pg_user = env_vars["POSTGRES_USER"]
pg_pwd = env_vars["POSTGRES_PASSWORD"]
ds_user = env_vars["DATASTORE_READONLY_USER"]
ds_pwd = env_vars["DATASTORE_READONLY_PASSWORD"]
pg_host = env_vars["POSTGRES_HOST"]
    
ckan_sqla_url = f"postgresql://{pg_user}:{pg_pwd}@{pg_host}/ckan?sslmode=disable"
ckan_ds_write_url = f"postgresql://{pg_user}:{pg_pwd}@{pg_host}/datastore?sslmode=disable"
ckan_ds_read_url = f"postgresql://{ds_user}:{ds_pwd}@{pg_host}/datastore?sslmode=disable"
test_ckan_sqla_url = f"postgresql://{pg_user}:{pg_pwd}@{pg_host}/ckan_test?sslmode=disable"
test_ckan_ds_write_url = f"postgresql://{pg_user}:{pg_pwd}@{pg_host}/datastore_test?sslmode=disable"
test_ckan_ds_read_url = f"postgresql://{ds_user}:{ds_pwd}@{pg_host}/datastore_test?sslmode=disable"


#print(env_vars['POSTGRES_USER'])

# Include .env values and create openshift yamls for build services
os.system('docker-compose config > docker-compose-resolved.yaml')
os.system(f'kompose --provider openshift --file docker-compose-resolved.yaml --build build-config --namespace {openshift_project} convert')

# Create folders
os.mkdir('openshift')
os.mkdir('openshift/build')
os.mkdir('openshift/build/imagestreams')
os.mkdir('openshift/build/others')
os.mkdir('openshift/build/ckan')
os.mkdir('openshift/build/nginx')
os.mkdir('openshift/build/trash')
os.mkdir('openshift/nonbuild')
os.mkdir('openshift/nonbuild/imagestreams')
os.mkdir('openshift/nonbuild/others')
os.mkdir('openshift/nonbuild/ckan')
os.mkdir('openshift/nonbuild/nginx')
os.mkdir('openshift/nonbuild/trash')

# Sort build services in folders
path = os.getcwd()
files = os.listdir(path)
for f in files:
    if "buildconfig.yaml" in f or "deploymentconfig.yaml" in f or "imagestream.yaml" in f or "service.yaml" in f or "persistentvolumeclaim.yaml" in f or "dev-namespace.yaml" in f:
        print(f)
        if "imagestream.yaml" in f:
            shutil.move(path + '/' + f, path + '/openshift/build/imagestreams/' + f )
        elif "imagestream.yaml" not in f and "dev-namespace.yaml" in f: 
            shutil.move(path + '/' + f, path + '/openshift/build/trash/' + f )
        elif "imagestream.yaml" not in f and "nginx" not in f and "ckan" not in f: 
            shutil.move(path + '/' + f, path + '/openshift/build/others/' + f )
        elif "imagestream.yaml" not in f and "nginx" in f: 
            shutil.move(path + '/' + f, path + '/openshift/build/nginx/' + f )
        elif "imagestream.yaml" not in f and "ckan" in f: 
            shutil.move(path + '/' + f, path + '/openshift/build/ckan/' + f )

# create openshift yamls for non-build services
os.system(f'kompose --provider openshift --file docker-compose-resolved.yaml --namespace {openshift_project} convert')

# Sort non-build services in folders
path = os.getcwd()
files = os.listdir(path)
for f in files:
    if "buildconfig.yaml" in f or "deploymentconfig.yaml" in f or "imagestream.yaml" in f or "service.yaml" in f or "persistentvolumeclaim.yaml" in f or "dev-namespace.yaml" in f:
        print(f)
        if "imagestream.yaml" in f:
            shutil.move(path + '/' + f, path + '/openshift/nonbuild/imagestreams/' + f )
        elif "imagestream.yaml" not in f and "dev-namespace.yaml" in f: 
            shutil.move(path + '/' + f, path + '/openshift/nonbuild/trash/' + f )
        elif "imagestream.yaml" not in f and "nginx" not in f and "ckan" not in f: 
            shutil.move(path + '/' + f, path + '/openshift/nonbuild/others/' + f )
        elif "imagestream.yaml" not in f and "nginx" in f: 
            shutil.move(path + '/' + f, path + '/openshift/nonbuild/nginx/' + f )
        elif "imagestream.yaml" not in f and "ckan" in f: 
            shutil.move(path + '/' + f, path + '/openshift/nonbuild/ckan/' + f )


# Individual adaptations

outfile_1 = 'openshift/capfile-1-imagestreams.yaml'
out_1 = open(outfile_1,'w')
outfile_2 = 'openshift/capfile-2-others.yaml'
out_2 = open(outfile_2,'w')
outfile_3 = 'openshift/capfile-3-ckan.yaml'
out_3 = open(outfile_3,'w')
outfile_4 = 'openshift/capfile-4-nginx.yaml'
out_4 = open(outfile_4,'w')

path_1 = path + '/openshift/build/imagestreams/'
path_1b = path + '/openshift/nonbuild/imagestreams/'

files = os.listdir(path_1)
for f in files:
    if "ckan" in f or "nginx" in f or "db" in f:
    #print(f)
        l = open(path_1 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_1.write(line.replace('apiVersion: v1','apiVersion: image.openshift.io/v1'))
        l.close()
        out_1.write('\n---\n\n')

files = os.listdir(path_1b)
for f in files:
    if "solr" in f or "datapusher" in f or "redis" in f:
    #print(f)
        l = open(path_1b + f,'r')
        lines = l.readlines()
        for line in lines:
            out_1.write(line.replace('apiVersion: v1','apiVersion: image.openshift.io/v1'))
        l.close()
        out_1.write('\n---\n\n')


path_2 = path + '/openshift/build/others/'
path_2b = path + '/openshift/nonbuild/others/'

files = os.listdir(path_2)
for f in files:
    #print(f)
    if "deploymentconfig.yaml" in f and "db" in f:
        #print(f)
        l = open(path_2 + f,'r')
        lines = l.readlines()
        for line in lines:   
            if 'claimName:' not in line:
                out_2.write(line.replace('persistentVolumeClaim:','emptyDir: {}').replace('apiVersion: v1','apiVersion: apps.openshift.io/v1'))
        l.close()
        out_2.write('\n---\n\n')

    elif "service.yaml" in f and "db" in f:
        #print(f)
        l = open(path_2 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_2.write(line)
        l.close()
        out_2.write('\n---\n\n')
    
    elif "buildconfig.yaml" in f in f and "db" in f:
        #print(f)
        l = open(path_2 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_2.write(line.replace('apiVersion: v1','apiVersion: build.openshift.io/v1')
            .replace('ref: main', branch_line)
            .replace('uri: https://git.muenchen.de/lhm-udp-katalog-2/ckan-docker-ga.git', repo_line)
            .replace('source:', source_secret_lines))
        l.close()
        out_2.write('\n---\n\n')

files = os.listdir(path_2b)
for f in files:
    #print(f)
    if "solr" in f or "redis" in f or "datapusher" in f:
        if "deploymentconfig.yaml" in f:
            #print(f)
            l = open(path_2 + f,'r')
            lines = l.readlines()
            for line in lines:   
                out_2.write(line.replace('claimName: solr-data','claimName: ckan-solr-pvc').replace('apiVersion: v1','apiVersion: apps.openshift.io/v1'))
            l.close()
            out_2.write('\n---\n\n')

        elif "service.yaml" in f and "db" in f:
         #print(f)
            l = open(path_2 + f,'r')
            lines = l.readlines()
            for line in lines:
                out_2.write(line)
            l.close()
            out_2.write('\n---\n\n')
    
        elif "buildconfig.yaml" in f in f and "db" in f:
            #print(f)
            l = open(path_2 + f,'r')
            lines = l.readlines()
            for line in lines:
                out_2.write(line.replace('apiVersion: v1','apiVersion: build.openshift.io/v1')
                .replace('ref: main', branch_line)
                .replace('uri: https://git.muenchen.de/lhm-udp-katalog-2/ckan-docker-ga.git', repo_line)
                .replace('source:', source_secret_lines))
            l.close()
            out_2.write('\n---\n\n')

switch = 0

path_3 = path + '/openshift/build/ckan/'
files = os.listdir(path_3)
for f in files:
    #print(f)
    if "deploymentconfig.yaml" in f:
        #print(f)
        l = open(path_3 + f,'r')
        lines = l.readlines()
        for line in lines:   
            if 'hostPort:' not in line:
                if 'protocol: TCP' not in line:

                    if '- name: POSTGRES_USER' in line:
                        switch = 1
                        secret_name = 'db-secret'
                        secret_key = 'postgres-user'

                    elif '- name: POSTGRES_PASSWORD' in line:
                        switch = 1
                        secret_name = 'db-secret'
                        secret_key = 'postgres-password'

                    elif '- name: DATASTORE_READONLY_USER' in line:
                        switch = 1
                        secret_name = 'db-secret'
                        secret_key = 'datastore-readonly-user'

                    elif '- name: DATASTORE_READONLY_PASSWORD' in line:
                        switch = 1
                        secret_name = 'db-secret'
                        secret_key = 'datastore-readonly-password'

                    elif '- name: POSTGRES_HOST' in line:
                        switch = 1
                        secret_name = 'db-secret'
                        secret_key = 'postgres-host'
                    
                    elif '- name: CKAN_SQLALCHEMY_URL' in line:
                        switch = 1
                        secret_name = 'db-secret'
                        secret_key = 'ckan-sqlalchemy-url'
                    
                    elif '- name: CKAN_DATASTORE_WRITE_URL' in line:
                        switch = 1
                        secret_name = 'db-secret'
                        secret_key = 'ckan-datastore-write-url'
                    
                    elif '- name: CKAN_DATASTORE_READ_URL' in line:
                        switch = 1
                        secret_name = 'db-secret'
                        secret_key = 'ckan-datastore-read-url'
                    
                    elif '- name: TEST_CKAN_SQLALCHEMY_URL' in line:
                        switch = 1
                        secret_name = 'db-secret'
                        secret_key = 'test-ckan-sqlalchemy-url'
                    
                    elif '- name: TEST_CKAN_DATASTORE_WRITE_URL' in line:
                        switch = 1
                        secret_name = 'db-secret'
                        secret_key = 'test-ckan-datastore-write-url'
                    
                    elif '- name: TEST_CKAN_DATASTORE_READ_URL' in line:
                        switch = 1
                        secret_name = 'db-secret'
                        secret_key = 'test-ckan-datastore-read-url'


                    if switch == 1 and 'value:' in line:                          
                        secret_lines = f'              valueFrom:\n                secretKeyRef:\n                  name: {secret_name}\n                  key: {secret_key}\n'
                        out_3.write(secret_lines)
                        switch = 0

                    else:
                        out_3.write(line.replace('claimName: ckan-storage','claimName: ckan-solr-pvc').replace('apiVersion: v1','apiVersion: apps.openshift.io/v1'))
        l.close()
        out_3.write('\n---\n\n')

    elif "service.yaml" in f:
        #print(f)
        l = open(path_3 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_3.write(line)
        l.close()
        out_3.write('\n---\n\n')
    
    elif "buildconfig.yaml" in f:
        #print(f)
        l = open(path_3 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_3.write(line.replace('apiVersion: v1','apiVersion: build.openshift.io/v1')
            .replace('ref: main', branch_line)
            .replace('uri: https://git.muenchen.de/lhm-udp-katalog-2/ckan-docker-ga.git', repo_line)
            .replace('source:', source_secret_lines))
        l.close()
        out_3.write('\n---\n\n')


path_4 = path + '/openshift/build/nginx/'
files = os.listdir(path_4)
for f in files:
    #print(f)
    if "deploymentconfig.yaml" in f:
        #print(f)
        l = open(path_4 + f,'r')
        lines = l.readlines()
        for line in lines:   
            if 'claimName:' not in line:
                if 'hostPort:' not in line:
                    if 'protocol: TCP' not in line:
                        out_4.write(line.replace('persistentVolumeClaim:','emptyDir: {}').replace('apiVersion: v1','apiVersion: apps.openshift.io/v1'))
        l.close()
        out_4.write('\n---\n\n')

    elif "service.yaml" in f:
        #print(f)
        l = open(path_4 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_4.write(line)
        l.close()
        out_4.write('\n---\n\n')
    
    elif "buildconfig.yaml" in f:
        #print(f)
        l = open(path_4 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_4.write(line.replace('apiVersion: v1','apiVersion: build.openshift.io/v1')
            .replace('ref: main', branch_line)
            .replace('uri: https://git.muenchen.de/lhm-udp-katalog-2/ckan-docker-ga.git', repo_line)
            .replace('source:', source_secret_lines))
        l.close()
        out_4.write('\n---\n\n')


# Add additional readymade yaml files for services and route

path_5 = path + '/openshift-add/'

files = os.listdir(path_5)
for f in files:
    if "ckan-route" not in f and "db-secret" not in f:
        #print(f)
        l = open(path_5 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_2.write(line.replace('udpkatalog-dev', openshift_project))
        l.close()
        out_2.write('\n---\n\n')
    
    elif "db-secret" in f:
        l = open(path_5 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_2.write(line.replace('POSTGRES_USER', env_vars['POSTGRES_USER'])\
                .replace('POSTGRES_PASSWORD', env_vars['POSTGRES_PASSWORD'])\
                .replace('DATASTORE_READONLY_USER', env_vars['DATASTORE_READONLY_USER'])\
                .replace('DATASTORE_READONLY_PASSWORD', env_vars['DATASTORE_READONLY_PASSWORD'])\
                .replace('POSTGRES_HOST', env_vars['POSTGRES_HOST'])\
                .replace('CKAN_SQLALCHEMY_URL', ckan_sqla_url)\
                .replace('CKAN_DATASTORE_WRITE_URL', ckan_ds_write_url)\
                .replace('CKAN_DATASTORE_READ_URL', ckan_ds_read_url)\
                .replace('TEST_CKAN_SQLALCHEMY_URL', test_ckan_sqla_url)\
                .replace('TEST_CKAN_DATASTORE_WRITE_URL', test_ckan_ds_write_url)\
                .replace('TEST_CKAN_DATASTORE_READ_URL', test_ckan_ds_read_url))

        l.close()
        out_2.write('\n---\n\n')

    elif "ckan-route" in f:
        #print(f)
        l = open(path_5 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_3.write(line.replace('udpkatalog-dev', openshift_project))
        l.close()
        out_3.write('\n---\n\n')

out_1.close()
out_2.close()
out_3.close()
out_4.close()


# Import the created  yaml files to openshift (CAP)
# Needs oc to be installed
# Make sure to be logged into openshift CLI and right project, check with "oc projects"

outfile_1 = 'openshift/capfile-1-imagestreams.yaml'
outfile_2 = 'openshift/capfile-2-others.yaml'
outfile_3 = 'openshift/capfile-3-ckan.yaml'
outfile_4 = 'openshift/capfile-4-nginx.yaml'

print('Import to Openshift part 1')

os.system('oc create -f ' + outfile_1)
os.system('oc create -f ' + outfile_2)

print('Builds and Deploys part 1 starting in CAP, waiting 60 seconds ... ')
time.sleep(60)

print('Import to Openshift part 2')

os.system('oc create -f ' + outfile_3)
os.system('oc create -f ' + outfile_4)

os.remove('docker-compose-resolved.yaml')
shutil.rmtree('openshift')

print('Ready, Builds and Deploys part 2 starting in CAP.')
