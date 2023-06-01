import requests
import json
import time


## User's variables
'''
You will need to define the following variables prior to creating your landing zone. 
Please gather and fill in all your information prior to running your script.
** input all as strings ** 
'''
# user_account = 'account@skytap.com' # Skytap user account
# API_key = '0000000' # API key or user account password
# env_region = 'Sample-Region' # Insert region name of your landing zone (see README)
# env_template = '0000000' # Insert region-based environment template ID
# env_name = 'Sample Name' # Assign preferred name to your new environment
# vm1_template = '0000000' # Insert region-based VM template ID
# vm2_template = '0000000' # Insert region-based VM template ID
# env_subnet = '10.0.0.0/24' # Define network subnet address range
# env_gateway = '10.0.0.254' # Define network gateway IPv4 address
# exr_name = 'Sample Name' # Assign preferred name to ExpressRoute circuit
# exr_key = '0000000' # Azure ExpressRoute service key
# remote_subnet = '10.1.0.0/24' # Remote subnet cannot overlap with environment's subnet

user_account = 'sarah_admin' # Skytap user account
API_key = 'ad61e8a4a1ecca7211c5f6f27f4136d13890a2fe' # API key or user account password
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

def skytap_url(type, env_id='', network_id='', exr_id=''):
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
    
    # To enable ExpressRoute
    elif type == 'temp_name':
        return url + f'vpns/{exr_id}'

    # To include remote subnet
    elif type == 'subnet':
        return url+ f'vpns/{exr_id}/subnets.json'
    
    # To attach environment's network to ExpressRoute
    elif type == 'network': # env_network
        return url + f'configurations/{env_id}/networks/{network_id}/vpns.json'

    # To connect environment's network to ExpressRoute
    elif type == 'exr': # env_network_exr
        return url + f'configurations/{env_id}/networks/{network_id}/vpns/{exr_id}.json'

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

'https://cloud.skytap.com/configurations/{env-id}/networks/{network-id}/vpns.json' --> WANs within network
    - Attach network to ExpressRoute

'https://cloud.skytap.com/configurations/{env_id}/networks/{network_id}/vpns/{exr_id}.json' --> ExpressRoute WAN
    - Connect environment's network to ExpressRoute
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
api_response = requests.put(skytap_url('environment', env_id=env_id), 
                            headers=headers,
                            auth=auth,
                            params={
                                 'template_id': vm1_template
                             })
http_status(api_response)

# LPAR/VM 2
api_response = requests.put(skytap_url('environment', env_id=env_id),
                            headers=headers,
                            auth=auth,
                            params={
                                'template_id': vm2_template
                            })
http_status(api_response)

## Check for busyness
# --> busyness function at top constants
# we have to check if all different URLs are busy
'''
-check if environment is busy
-change network on environment
-check if network is busy
-attach environment network to EXR/VPN/WAN
-check if EXR/VPN/WAN is busy
-connect environment network to EXR/VPN/WAN
'''

skytap_url = ''
def busyness(skytap_url):
    i = 0
    check = get_env()

    while i is not 3 and check['busy'] is not None:
        print('busy loop')
        i += 1
        check = get_env()
        time.sleep(3)
        
        return check

def get_env():
    return requests.get(skytap_url('configurations'),
                             headers=headers,
                             auth=auth,
                             )

## Configure environment network
api_response = requests.put(skytap_url('environment', env_id=env_id),
                            headers=headers,
                            auth=auth,
                            params={
                                'subnet': env_subnet
                            })
http_status(api_response)
network_id = api_response['id']


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


## Attach network to private network connection
api_response = requests.post(skytap_url('network', env_id=env_id, network_id=network_id),
                             auth=auth,
                             params={
                                 'vpn_id': exr_id
                             })
http_status(api_response)


## Include remote subnet
api_response = requests.post(skytap_url('subnet', exr_id=exr_id),
                             auth=auth,
                             params={
                                 'cidr_block': remote_subnet
                             })


## Connect environment's network to ExpressRoute/WAN
api_response = requests.put(skytap_url('exr', env_id=env_id, network_id=network_id, exr_id=exr_id),
                            auth=auth,
                            params={
                                'connected': True
                            })
http_status(api_response)


## Enable ExpressRoute
api_response = requests.put(skytap_url('temp_name', exr_id=exr_id),
                            auth=auth,
                            params={
                                'enabled': True
                            })



## (?) do we want to send a GET request at the end for user to look at their new configurations?
#   --> incorporate URL that takes to Skytap interface in GET response


# --> Function to check if environment is busy + 
#       - we cannot make changes to network while it is busy
#       - runstate field == "stopped" so you can proceed
#       - retry command every 10 seconds