import requests
import json


## User's variables
'''
You will need to define the following variables prior to creating your landing zone. 
Please gather and fill in all your information prior to running your script.
** input all as strings ** 
'''
user_account = 'sarahallen@skytap.com_5826' # Skytap user account
API_key = '5ab1633066ee7bef2fe4fc7372e01713b0e4f71e' # API key or user account password
env_region = 'US-Texas-M-1' # Insert region name of your landing zone (see README)
env_template = '2110325' # Insert region-based environment template ID
env_name = 'Test-Env-Ihovanna' # Assign preferred name to your new environment
vm1_template = '2110325' # Insert region-based VM template ID
vm2_template = '2111381' # Insert region-based VM template ID
env_subnet = '10.0.0.0/24' # Define network subnet address range
env_gateway = '10.0.0.254' # Define network gateway IPv4 address
exr_name = 'Test-ExR-Ihovanna' # Assign preferred name to ExpressRoute circuit
exr_key = '9521a609-27ec-4aae-8388-9921807d82d8' # Azure ExpressRoute service key


## Constants
'''
These variables and functions will be constantly used throughout the script.
Do not modify them. 
'''

url = 'https://cloud.skytap.com/'
auth = (user_account, API_key)
headers = { 'Accept': 'application/json', 'Content-type': 'application/json'}

def skytap_url(type, env_id=''):
    # To create new environments
    if type == 'configurations':
        return url + 'configurations.json'

    # To create new LPARs or VMs
    # To modify network configuration
    elif type == 'environment':
        return url + f'configurations/{env_id}.json'

    # To generate public IP address
    elif type == 'ip_address':
        return url + 'ips/acquire.json'

    # To create WANs/Azure ExpressRoute
    elif type == 'wan':
        return url + 'vpns.json'
    
    else:
        raise TypeError('Must specify a valid type of operation to continue.')

'''
'https://cloud.skytap.com/configurations.json' --> all environments
    - Create an environment

'https://cloud.skytap.com/configurations/{env_id}.json' --> within an env
    - Create new LPARs and VMs
    - Configure network

'https://cloud.skytap.com/ips/acquire.json' --> IP addresses
    - Generate an public IP address (???)

'https://cloud.skytap.com/vpns.json' --> WAN resources
    - Create new ExpressRoute
'''

def http_status(response):
    return 'HTTP status_code = %s' % response.status_code
    ## (?) Do we want this to return a description of the successfull operation at all or just the code?

def id_str(response, operation):
    if response and response.status_code == 200:
        data = response.json()
        return str(data['id'])
    
    else:
        raise RuntimeError(f'Unable to create {operation}')


## Create a new environment
api_response = requests.post(skytap_url('configurations'),
                             headers=headers,
                             auth=auth,
                             params={
                                 'template_id': env_template,
                                 'name': env_name,
                             })
http_status(api_response)
json_output = json.loads(api_response.text)
print(json.dumps(json_output, indent = 4))

env_id = id_str(api_response, 'environment')
print('environment_id = %s' % env_id)


## Add LPARs/VMs to environment
# LAPR/VM 1
api_response = requests.put(skytap_url('environment', env_id), 
                            headers=headers,
                            auth=auth,
                            params={
                                 'template_id': vm1_template
                             })
http_status(api_response)

# LPAR/VM 2
api_response = requests.put(skytap_url('environment', env_id),
                            headers=headers,
                            auth=auth,
                            params={
                                'template_id': vm2_template
                            })
http_status(api_response)


## Configure environment network
api_response = requests.put(skytap_url('environment', env_id),
                            headers=headers,
                            auth=auth,
                            params={
                                'subnet': env_subnet
                            })
http_status(api_response)


## Acquire public IP in same region as environment
api_response = requests.post(skytap_url('ip_address'),
                             headers=headers,
                             auth=auth,
                             params={
                                 'region': env_region
                             })
http_status(api_response)
public_ip_id = id_str(api_response, 'public IP')
print('public_ip_id = %s' % public_ip_id)


## Add ExpressRoute in same region as environment
api_response = requests.post(skytap_url('wan'),
                             headers=headers,
                             auth=auth,
                             params={
                                'name': exr_name,
                                'region': env_region,
                                'connection-managed-by': 'customer',
                                'service_key': exr_key,
                                'local_peer_ip': public_ip_id,
                                'local_subnet': env_subnet,
                                'nat_local_subnet': 'false',
                                'connection_type': 'express_route',
                                'phase_2_perfect_forward_secrecy': 'false',
                                'specify_maximum_segment_size': 'false',
                                'maximum_segment_size': 'null',
                                'dpd_enabled': 'false',
                                'route_based': 'false',
                                'sa_policy_level': 'null'
                                })
http_status(api_response)
exr_id = id_str(api_response, 'ExpressRoute connection')
print('exr_id = %s' % exr_id)


## Function to connect envs to ExpressRoute + enable ExpressRoute
# attach then connect the environment network to the WAN
# https://help.skytap.com/API_Documentation.html#Network
# https://help.skytap.com/wan-connecting-environments.html

## (?) do we want to send a GET request at the end for user to look at their new configurations?
#   --> incorporate URL that takes to Skytap interface in GET response
