import requests
import json


## define the requesite url, headers, and authorization for the Skytap API ##
url = 'https://cloud.skytap.com/' # instance URL for Skytap account
urlv2 = 'https://cloud.skytap.com/v2/configurations'
auth = ('sarahallen@skytap.com_5826', '9958debb7de6489f1292b2cdfa5154c22386120c') # login and password/API Token
headers = { 'Accept': 'application/json', 'Content-type': 'application/json'}

#template variables to be used for environment creation
template_ibmi74 = "2110325" #ibmi 7.4 Skytap template id, US-Texas-M-1 region
template_windows = "2111381" #Windows 2022 Skytap template id, US-Texas-M-1 region


## GET and print the results ##
#api_response = requests.get(url + '/126296058', headers=headers, auth=auth)
#print("HTTP status_code = %s" % api_response.status_code)

# next two lines make the json response pretty
#json_output = json.loads(api_response.text)
#print(json.dumps(json_output, indent = 4))

# create new environment using Skytap 7.4 template
template_params = {"template_id": template_ibmi74, "name":"IBMi 7.4 Migration Environment"}

api_response = requests.post(url + 'configurations.json', headers=headers, auth=auth, params=template_params)
print("HTTP status_code = %s" % api_response.status_code)

json_output = json.loads(api_response.text)
print(json.dumps(json_output, indent = 4))

#if environment creation is successful, get environment id
json_data = api_response.json() if api_response and api_response.status_code== 200 else None
if json_data and 'id' in json_data:
    env_id = json_data["id"]
    print(env_id)

#use environment id to add a new NFS LPAR to the environment, using Skytap IBMi 7.4 template
template_params = {"template_id": template_ibmi74}

api_response = requests.put(url + 'configurations/' + env_id + '.json', headers=headers, auth=auth, params=template_params)
print("HTTP status_code = %s" % api_response.status_code)

#add a new Windows jump host to the environment, using Skytap Windows 2022 template
template_params = {"template_id": template_windows}

api_response = requests.put(url + 'configurations/' + env_id + '.json', headers=headers, auth=auth, params=template_params)
print("HTTP status_code = %s" % api_response.status_code)

#optional function to edit skytap network 
env_subnet = "10.1.0.0/24"
env_gateway = "10.1.0.254"
environment_params = {"subnet": env_subnet}
api_response = requests.put(url + 'configurations/' + env_id + '.json', headers=headers, auth=auth, params=environment_params)
print("HTTP status_code = %s" % api_response.status_code)

#acquire public ip to account in same region as environment
ip_params = {"region": "US-Texas-M-1"} #Skytap regions listed in https://help.skytap.com/API_Documentation.html#Public

api_response = requests.post(url + 'ips/acquire.json', headers=headers, auth=auth, params=ip_params)
#if public IP creation is successful, get environment id
json_data = api_response.json() if api_response and api_response.status_code== 200 else print("public ip not created. have you reached your account IP limit?")
if json_data and 'id' in json_data:
    pubip_id = json_data["id"]
    print(pubip_id)

#add expressroute to account in same region as environment
exr_servicekey = "efc4f2b1-41d0-40b0-8756-a69d552db86a" #service key from provisioned expressroute
exr_region = "US-Texas-M-1"
exr_params = {
  "name": "Sarah via API",
  "region": exr_region,
  "connection-managed-by": "customer",
  "service_key": exr_servicekey,
  "local_peer_ip": pubip_id,
  "local_subnet": env_subnet,
  "nat_local_subnet": "false",
  "connection_type": "express_route",
  "phase_2_perfect_forward_secrecy": "false",
  "specify_maximum_segment_size": "false",
  "maximum_segment_size": "null",
  "dpd_enabled": "false",
  "route_based": "false",
  "sa_policy_level": "null"
}

api_response = requests.post(url + 'vpns.json', headers=headers, auth=auth, params=exr_params)
#if exr creation is successful, get exr id
json_data = api_response.json() if api_response and api_response.status_code== 200 else print("expressroute connection not created")
if json_data and 'id' in json_data:
    exr_id = json_data["id"]
    print(exr_id)

#check for expressroute to finish provisioning

#attach environment to expressroute 


