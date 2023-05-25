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
exr_key = '0000000' # ExpressRoute service key
exr_region = '' # (?) same as all Skytap's envs' regions????? ****
env_region = '' # Insert region name of your landing zone
env_template = '0000000' # Insert region-based environment template ID
env_name = 'Sample Name' # Assign preferred name to your new environment
vm_template = '0000000' # Insert region-based VM template ID
env_subnet = '10.0.0.0/24' # Define network subnet address range
env_gateway = '10.0.0.254' # Define network gateway IPv4 address


## Constants
'''
These variables  wil be constantly used throughout the script.
Do not modify them. 
'''

url = 'https://cloud.skytap.com/'
auth = (user_account, API_key)
headers = { 'Accept': 'application/json', 'Content-type': 'application/json'}