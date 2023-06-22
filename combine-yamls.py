## Translate ckan-docker to openshift input files for LHM CAP with kompose and adaptations
## Needs docker-compose and kompose to be installed
## Import the resulting capfiles to openshift with 'oc create -f ..'
## For that, be sure to be logged into openshift and right project, check with "oc projects"

import os
import shutil

## Insert repo with dockerfiles to be used for buildconfig:
repo = 'uri: https://github.com/gislab-augsburg/ckan-docker.git'
branch = 'ref: openshift' 

# Include .env values and create openshift yamls
os.system('docker-compose config > docker-compose-resolved.yaml')
os.system('kompose --provider openshift --file docker-compose-resolved.yaml --build build-config convert')

# Sort yamls in folders
os.mkdir('openshift')
os.mkdir('openshift/imagestreams')
os.mkdir('openshift/others')
os.mkdir('openshift/ckan')
os.mkdir('openshift/nginx')

path = os.getcwd()
files = os.listdir(path)
for f in files:
    if "buildconfig.yaml" in f or "deploymentconfig.yaml" in f or "imagestream.yaml" in f or "service.yaml" in f or "persistentvolumeclaim.yaml" in f:
        print(f)
        if "imagestream.yaml" in f:
            shutil.move(path + '/' + f, path + '/openshift/imagestreams/' + f )
        elif "imagestream.yaml" not in f and "nginx" not in f and "ckan" not in f: 
            shutil.move(path + '/' + f, path + '/openshift/others/' + f )
        elif "imagestream.yaml" not in f and "nginx" in f: 
            shutil.move(path + '/' + f, path + '/openshift/nginx/' + f )
        elif "imagestream.yaml" not in f and "ckan" in f: 
            shutil.move(path + '/' + f, path + '/openshift/ckan/' + f )


# Adaptations

outfile_1 = 'openshift/capfile-1-imagestreams.yaml'
out_1 = open(outfile_1,'w')
outfile_2 = 'openshift/capfile-2-others.yaml'
out_2 = open(outfile_2,'w')
outfile_3 = 'openshift/capfile-3-ckan.yaml'
out_3 = open(outfile_3,'w')
outfile_4 = 'openshift/capfile-4-nginx.yaml'
out_4 = open(outfile_4,'w')

path_1 = path + '/openshift/imagestreams/'
files = os.listdir(path_1)
for f in files:
    #print(f)
    l = open(path_1 + f,'r')
    lines = l.readlines()
    for line in lines:
        out_1.write(line.replace('apiVersion: v1','apiVersion: image.openshift.io/v1'))
    l.close()
    out_1.write('\n---\n\n')


path_2 = path + '/openshift/others/'
files = os.listdir(path_2)
for f in files:
    #print(f)
    if "deploymentconfig.yaml" in f:
        #print(f)
        l = open(path_2 + f,'r')
        lines = l.readlines()
        for line in lines:   
            if 'claimName:' not in line:
                out_2.write(line.replace('persistentVolumeClaim:','emptyDir: {}').replace('apiVersion: v1','apiVersion: apps.openshift.io/v1'))
        l.close()
        out_2.write('\n---\n\n')

    elif "service.yaml" in f:
        #print(f)
        l = open(path_2 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_2.write(line)
        l.close()
        out_2.write('\n---\n\n')
    
    elif "buildconfig.yaml" in f:
        #print(f)
        l = open(path_2 + f,'r')
        lines = l.readlines()
        for line in lines:
            out_2.write(line.replace('apiVersion: v1','apiVersion: build.openshift.io/v1').replace('ref: main', branch).replace('uri: https://git.muenchen.de/lhm-udp-katalog-2/ckan-docker-ga.git', repo))
        l.close()
        out_2.write('\n---\n\n')


path_3 = path + '/openshift/ckan/'
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


path_4 = path + '/openshift/nginx/'
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

out_1.close()
out_2.close()
out_3.close()
out_4.close()



    
