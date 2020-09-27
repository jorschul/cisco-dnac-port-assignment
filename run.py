__author__ = "Oren Brigg"
__author_email__ = "obrigg@cisco.com"
__copyright__ = "Copyright (c) 2020 Cisco Systems, Inc."

import time
from webexteamssdk import WebexTeamsAPI
from dnacentersdk import api
from pprint import pprint
from dnac_config import *

def CheckProject(projectX):
    projects = dnac.configuration_templates.get_projects()
    for project in projects:
        if project['name'] == projectX:
            return (project['id'])
    # If project does not exist:
    return(CreateProject(projectX))

def CreateProject(projectX):
    taskId = dnac.configuration_templates.create_project(name=projectX)
    time.sleep(2)
    taskStatus = dnac.task.get_task_by_id(taskId['response']['taskId'])
    if taskStatus['isError'] == True:
        raise Exception (" **** Project Creation FAILED ****")
    return(taskStatus['data'])
    
def CheckTemplate(projectId, templateX):
    templates = dnac.configuration_templates.gets_the_templates_available()
    for template in templates:
        if template['name'] == templateX:
            return (template['templateId'])
    return(CreateTemplate(projectId, templateX))

def CreateTemplate(projectId, templateX):
    content = """!
        interface $int
        switchport access vlan $vlan
        """
    templateParams = [{'parameterName': 'vlan', 'dataType': 'INTEGER', 'defaultValue': None, 
        'description': None, 'required': True, 'notParam': False, 'paramArray': False, 
        'displayName': None, 'instructionText': None, 'group': None, 'order': 2, 
        'selection': None, 'range': [], 'key': None, 'provider': None, 'binding': ''}, 
        {'parameterName': 'int', 'dataType': 'STRING', 'defaultValue': None, 
        'description': None, 'required': True, 'notParam': False, 'paramArray': False, 
        'displayName': None, 'instructionText': None, 'group': None, 'order': 1, 
        'range': [], 'key': None, 'provider': None, 'binding': ''}]
    taskId = dnac.configuration_templates.create_template(project_id=projectId, name=templateX, 
        composite=False, deviceTypes=[{'productFamily': 'Switches and Hubs'}], 
        softwareType="IOS-XE", templateContent=content)
    time.sleep(2)
    taskStatus = dnac.task.get_task_by_id(taskId['response']['taskId'])
    if taskStatus['isError'] == True:
        raise Exception (" **** Template Creation FAILED ****")
    templateId = taskStatus['response']['data']
    # Commit the template
    taskId = dnac.configuration_templates.version_template(templateId=templateId, comments="Initial commit")
    time.sleep(2)
    taskStatus = dnac.task.get_task_by_id(taskId['response']['taskId'])
    if taskStatus['isError'] == True:
        raise Exception (" **** Template Creation FAILED ****")
    return(taskStatus['response']['data'])

def DeployTemplate(templateId, deviceIp, params):
    targetInfo = [{'id': deviceIp, 'type': "MANAGED_DEVICE_IP", "params": params}]
    taskId = dnac.configuration_templates.deploy_template(forcePushTemplate=True, 
        isComposite=False, templateId=templateId, targetInfo=targetInfo)
    time.sleep(2)
    taskStatus = dnac.task.get_task_by_id(taskId['response']['taskId'])

if __name__ == "__main__":
    # User inputs
    dnac_version = "1.3.3"
    project_name = "Vlan Assignment"
    template_name = "int_vlan"
    deviceIp = "99.99.99.106"
    params = {'vlan': '20', 'interface': 'gig1/0/33'}
    # Connecting to DNAC
    dnac = api.DNACenterAPI(username=DNAC_USER,
                            password=DNAC_PASSWORD,
                            base_url="https://" + DNAC + ":" + str(DNAC_PORT),
                            version=dnac_version,
                            verify=False)
    #
    projectId = CheckProject(project_name)
    templateId = CheckTemplate(projectId, template_name)
    DeployTemplate(templateId, deviceIp, params)
