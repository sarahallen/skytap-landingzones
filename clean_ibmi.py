import requests
import json



## User's variables
'''
You will need to define the following variables prior to creating your landing zone. 
Please gather and fill in all your information prior to running your script.
** input all as strings ** 
'''
user_account = 'account@skytap.com' # Skytap user account
API_key = 'numbers' # API key or user accoutn password


## Constants
'''
These variables  wil be constantly used throughout the script.
Do not modify them. 
'''

url = 'https://cloud.skytap.com/'
auth = (user_account, API_key)
headers = { 'Accept': 'application/json', 'Content-type': 'application/json'}