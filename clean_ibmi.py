import requests
import json


## User's variables
'''
You will need to define the following variables prior to creating your landing zone. 
Please gather and fill in all your information prior to running your script.
** input all as strings ** 
'''
user_account = 'account@skytap.com' # Skytap user account
API_key = '0000000' # API key or user account password
env_region = '' # Insert region name of your landing zone (see README)
env_template = '0000000' # Insert region-based environment template ID
env_name = 'Sample Name' # Assign preferred name to your new environment
vm_template = '0000000' # Insert region-based VM template ID
env_subnet = '10.0.0.0/24' # Define network subnet address range
env_gateway = '10.0.0.254' # Define network gateway IPv4 address
# ^ (?) does not get used in this scripted case, should it??????
exr_name = '' # Assign preferred name to ExpressRoute circuit
exr_region = '' # (?) same as Skytap's envs' regions????? ****
exr_key = '0000000' # Azure ExpressRoute service key


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
        raise('Must specify a valid type of operation to continue.')

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

def print_response(response, variable, operation):
    if response and response.status_code == 200:
        data = response.json()
        id = data['id']
        return f'{variable} = {id}'
    
    else:
        return f'Unable to create {operation}'


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
print_response(api_response, 'environment_id', 'environment')


## Add LPARs/VMs to environment
# LAPR/VM 1
env_id = api_response.json()['id']
api_response = requests.put(skytap_url('environment', env_id), 
                            headers=headers,
                            auth=auth,
                            params={
                                 'template_id': vm_template
                             })
http_status(api_response)

# LPAR/VM 2
api_response = requests.put(skytap_url('environment', env_id),
                            headers=headers,
                            auth=auth,
                            params={
                                'template_id': vm_template
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
print_response(api_response, 'public_ip_id', 'public IP')


## Add ExpressRoute in same region as environment
api_response = requests.post(skytap_url('wan')
                             headers=headers,
                             auth=auth,
                             params={
                                'name': exr_name,
                                'region': exr_region,
                                'connection-managed-by': 'customer',
                                'service_key': exr_servicekey,
                                'local_peer_ip': public_ip_id,
                                "local_subnet": env_subnet,
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
print_response(api_response, 'exr_id', 'ExpressRoute connection')


