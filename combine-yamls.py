## Translate ckan-docker to openshift input yaml files for LHM CAP with kompose and adaptations
## Needs docker-compose and kompose to be installed
## Import the resulting capfiles to openshift with 'oc create -f ..'
## For that, be sure to be logged into openshift and right project, check with "oc projects"

import os
import shutil

## Insert repo with dockerfiles to be used for buildconfig:
repo = 'uri: https://github.com/gislab-augsburg/ckan-docker.git'
branch = 'ref: openshift' 

# Include .env values and create openshift yamls for build services
os.system('docker-compose config > docker-compose-resolved.yaml')
os.system('kompose --provider openshift --file docker-compose-resolved.yaml --build build-config convert')

# Create folders
os.mkdir('openshift')
os.mkdir('openshift/build')
os.mkdir('openshift/build/imagestreams')
os.mkdir('openshift/build/others')
os.mkdir('openshift/build/ckan')
os.mkdir('openshift/build/nginx')
os.mkdir('openshift/nonbuild')
os.mkdir('openshift/nonbuild/imagestreams')
os.mkdir('openshift/nonbuild/others')
os.mkdir('openshift/nonbuild/ckan')
os.mkdir('openshift/nonbuild/nginx')

# Sort build services in folders
path = os.getcwd()
files = os.listdir(path)
for f in files:
    if "buildconfig.yaml" in f or "deploymentconfig.yaml" in f or "imagestream.yaml" in f or "service.yaml" in f or "persistentvolumeclaim.yaml" in f:
        print(f)
        if "imagestream.yaml" in f:
            shutil.move(path + '/' + f, path + '/openshift/build/imagestreams/' + f )
        elif "imagestream.yaml" not in f and "nginx" not in f and "ckan" not in f: 
            shutil.move(path + '/' + f, path + '/openshift/build/others/' + f )
        elif "imagestream.yaml" not in f and "nginx" in f: 
            shutil.move(path + '/' + f, path + '/openshift/build/nginx/' + f )
        elif "imagestream.yaml" not in f and "ckan" in f: 
            shutil.move(path + '/' + f, path + '/openshift/build/ckan/' + f )

# create openshift yamls for non-build services
os.system('kompose --provider openshift --file docker-compose-resolved.yaml convert')

# Sort non-build services in folders
path = os.getcwd()
files = os.listdir(path)
for f in files:
    if "buildconfig.yaml" in f or "deploymentconfig.yaml" in f or "imagestream.yaml" in f or "service.yaml" in f or "persistentvolumeclaim.yaml" in f:
        print(f)
        if "imagestream.yaml" in f:
            shutil.move(path + '/' + f, path + '/openshift/nonbuild/imagestreams/' + f )
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
            out_2.write(line.replace('apiVersion: v1','apiVersion: build.openshift.io/v1').replace('ref: main', branch).replace('uri: https://git.muenchen.de/lhm-udp-katalog-2/ckan-docker-ga.git', repo))
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
                out_2.write(line.replace('apiVersion: v1','apiVersion: build.openshift.io/v1').replace('ref: main', branch).replace('uri: https://git.muenchen.de/lhm-udp-katalog-2/ckan-docker-ga.git', repo))
            l.close()
            out_2.write('\n---\n\n')


path_3 = path + '/openshift/build/ckan/'
files = os.listdir(path_3)
for f in files:
    #print(f)
    if "deploymentconfig.yaml" in f:
        #print(f)
        l = open(path_3 + f,'r')
        lines = l.readlines()
        for line in lines:   
            if 'claimName:' not in line:
                out_3.write(line.replace('persistentVolumeClaim:','emptyDir: {}').replace('apiVersion: v1','apiVersion: apps.openshift.io/v1'))
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
            out_3.write(line.replace('apiVersion: v1','apiVersion: build.openshift.io/v1').replace('ref: main', branch).replace('uri: https://git.muenchen.de/lhm-udp-katalog-2/ckan-docker-ga.git', repo))
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
            out_4.write(line.replace('apiVersion: v1','apiVersion: build.openshift.io/v1').replace('ref: main', branch).replace('uri: https://git.muenchen.de/lhm-udp-katalog-2/ckan-docker-ga.git', repo))
        l.close()
        out_4.write('\n---\n\n')


# Add additional readymade yaml files for services and route

path_5 = path + '/openshift_add/'

files = os.listdir(path_5)
for f in files:
    if "ckan" not in f:
        #print(f)
        l = open(path_5 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_2.write(line)
        l.close()
        out_2.write('\n---\n\n')

    elif "ckan" in f:
        #print(f)
        l = open(path_5 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_3.write(line)
        l.close()
        out_3.write('\n---\n\n')

out_1.close()
out_2.close()
out_3.close()
out_4.close()



    
