
## Import the created capfiles to openshift.
## Needs oc to be installed.
## Make sure to be logged into openshift CLI and right project, check with "oc projects".

import os

outfile_1 = 'openshift/capfile-1-imagestreams.yaml'
outfile_2 = 'openshift/capfile-2-others.yaml'
outfile_3 = 'openshift/capfile-3-ckan.yaml'
outfile_4 = 'openshift/capfile-4-nginx.yaml'

print(outfile_1)

#os.system('oc create -f ' + outfile_1)
#os.system('oc create -f ' + outfile_2)
os.system('oc create -f ' + outfile_3)
os.system('oc create -f ' + outfile_4)