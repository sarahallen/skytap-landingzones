import requests 
import json

## Sarah's Credentials
user_account = 'ihovannahuezo@skytap.com' # Skytap user account
API_key = '3198247fb000e825199bc82c2591170aa21d30cd' # API key or user account password
env_region = 'US-East-2' # Insert region name of your landing zone (see README)
env_template = '2245235' # Insert region-based environment template ID
env_name = 'API-Test-Env' # Assign preferred name to your new environment
vm1_template = '146508618' # Insert region-based VM template ID
vm2_template = '2111381' # Insert region-based VM template ID
env_subnet = '10.0.0.0/24' # Define network subnet address range
env_gateway = '10.0.0.254' # Define network gateway IPv4 address
exr_name = 'API-Test-ExR' # Assign preferred name to ExpressRoute circuit
exr_key = '' # Azure ExpressRoute service key


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
    
    # To attach environment's network to ExpressRoute
    elif type == 'network':
        return url + f'configurations/{env_id}/networks/{network_id}/vpns.json'

    # To connect environment's network to ExpressRoute
    elif type == 'exr':
        return url + f'configurations/{env_id}/networks/{network_id}/vpns/{exr_id}.json'

    else:
        raise TypeError('Must specify a valid type of operation to continue.')


def id_str(response, operation):
    if response and response.status_code == 200:
        data = response.json()
        return str(data['id'])
    
    else:
        raise RuntimeError(f'Unable to create {operation}')


## Create environment
api_response = requests.post(skytap_url('configurations'),
                             headers=headers,
                             auth=auth,
                             params={
                                 'template_id': env_template,
                                 'name': env_name,
                             })

env_id = id_str(api_response, 'environment')
print('environment_id = %s' % env_id)

## Get all networks within environment
r = requests.get('https://cloud.skytap.com/configurations/{configuration-id}/networks')
json_output = json.loads(api_response.text)
print(json.dumps(json_output, indent = 4))

# app_response['networks'][0]['id']

## Delete environment
requests.delete(skytap_url('environment', env_id=env_id),
                             headers=headers,
                             auth=auth,
                             params={
                                 'template_id': env_template,
                                 'name': env_name,
                             })