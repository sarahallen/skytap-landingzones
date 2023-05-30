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
env_region = '' # Insert region name of your landing zone
env_template = '0000000' # Insert region-based environment template ID
env_name = 'Sample Name' # Assign preferred name to your new environment
vm_template = '0000000' # Insert region-based VM template ID
env_subnet = '10.0.0.0/24' # Define network subnet address range
env_gateway = '10.0.0.254' # Define network gateway IPv4 address
exr_key = '0000000' # Azure ExpressRoute service key
exr_region = '' # (?) same as Skytap's envs' regions????? ****


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
        raise('Must specify type of operation to continue.')

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


## Create a new environment
api_response = requests.post(skytap_url('configurations'),
                             headers=headers,
                             auth=auth,
                             params={
                                 'template_id': env_template,
                                 'name': env_name,
                             })

print('HTTP status_code = %s' % api_response.status_code)
json_output = json.loads(api_response.text)
print(json.dumps(json_output, indent = 4))

json_data = api_response.json() if api_response and api_response.status_code== 200 else None
env_id = json_data['id'] if json_data and 'id' in json_data else None
print('environment_ID = %s' % env_id)


## Add LPARs/VMs to environment
# LAPR/VM 1
api_response = requests.put(skytap_url('environment', env_id), 
                            headers=headers,
                            auth=auth,
                            params={
                                 'template_id': vm_template
                             })

print("HTTP status_code = %s" % api_response.status_code)

# LPAR/VM 2
api_response = requests.put(skytap_url('environment', env_id),
                            headers=headers,
                            auth=auth,
                            params={
                                'template_id': vm_template
                            })

print("HTTP status_code = %s" % api_response.status_code)