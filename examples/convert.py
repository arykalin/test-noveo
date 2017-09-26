configMapFile='someproject.yaml'
deployementFiles=[
    'k8s/someproject-address-deployment.yaml',
    'k8s/someproject-back-deployment.yaml',
    'k8s/someproject-customer-deployment.yaml',
    'k8s/someproject-service-deployment.yaml',
    'k8s/docker-example-deployment.yaml'
]

import yaml
import json
import time

timestamp = int(time.time())
class processConfigMApEnvironemtToDeployement(object):
    def __init__(self, configMapName, deploymentDict):
        self.configMapName = configMapName
        self.deploymentDict = deploymentDict
    def cleanUp(self):
        #Cleanup
        a=deploymentDict['spec']['template']['spec']['containers'][0]['env']
        for item in a[:]:
            if 'valueFrom' in item:
                print("Removing : {}".format(item))
                deploymentDict['spec']['template']['spec']['containers'][0]['env'].remove(item)
        return deploymentDict

    def fillUp(self):
        # Filling up with new values
        l = []
        for e in configMapDict['data']:
            l.append(e)
        for e in sorted(l):
            # for e in configMapDict['data']:
            envTemplate = json.loads(
                '{"name": "ENV_NAME","valueFrom": {"configMapKeyRef": {"name": "configMapName","key": "ENV_NAME"}}}')
            envTemplate['name'] = e
            envTemplate['valueFrom']['configMapKeyRef']['key'] = e
            envTemplate['valueFrom']['configMapKeyRef']['name'] = configMapName
            print("Adding : {}".format(envTemplate))
            deploymentDict['spec']['template']['spec']['containers'][0]['env'].append(envTemplate)
        return deploymentDict


configMapName=configMapFile.split(".")[0]
configMapName=configMapName+'-'+str(timestamp)

with open(configMapFile) as f:
    configMapDict = yaml.load(f)

configMapDict['metadata']['name']=configMapName
with open(configMapFile, 'w') as f:
    yaml.dump(configMapDict, f,default_flow_style=False)

for deployementFile in deployementFiles:
    print("############################Processing {}".format(deployementFile))
    with open(deployementFile) as f:
        deploymentDict = yaml.load(f)
    a = processConfigMApEnvironemtToDeployement(configMapName, deploymentDict)
    deploymentDict=a.cleanUp()
    deploymentDict=a.fillUp()
    with open(deployementFile, 'w') as f:
        yaml.dump(deploymentDict, f, default_flow_style=False)
