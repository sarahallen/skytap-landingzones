# Skytap Landing Zones #
Get started with Skytap Environment creation using the Rest API.

These scripts use Skytap Python REST API v1 to perform the following operations:
- Deliver a summary of all existing environments within a Skytap account. 
- Create a new environment within a Skytap account.
- Create two LPARs/VMs within an existing environment. 
- Configure the environment's network.
- Acquire a public IP for account.
- Add an ExpressRoute circuit WAN to environment. 

## Pre-Requisites: ##
* An active Skytap account or Skytap on Azure services. 
* Skytap account email address or Skytap on Azure auto-generated email address. 
* Skytap REST API key or Skytap account password.
* An active Azure ExpressRoute service key. 
* May need to install `requests` library.

## How to run this script ##
Set up your Azure ExpressRoute prior to running this script. You can utilize your 
Azure portal ot the following Azure Networking scripts on GitHub: 
https://github.com/poomnupong/azure-networking.git

We recommend running this Skytap Landing Zones script in you Azure account's PowerShell. 

Alternatively, you can clone this repo, save it to your machine, 
then upload the script to your Azure account's PowerShell. 
For a more detailed set of steps, follow:
https://learn.microsoft.com/en-us/azure/cloud-shell/persisting-shell-storage#upload-files

### Skytap Regions ###
    - APAC-2
    - AU-Sydney-I-1
    - CAN-Toronto
    - CN-HongKong-M-1 
    - DE-Frankfurt-1-1
    - EMEA
    - IE-Dublin-M-1
    - NL-Amsterdam-M-1 
    - SG-Singapore-M-1
    - UK-Londond-M-1
    - US-Central 
    - US-East-2
    - US-Texas-M-1
    - US-Virginia-M-1
    - US-West

#### Skytap REST API v1 documentation:
https://help.skytap.com/API_Documentation.html#top


#### API Request endpoints utilized: ####
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


#### Disclaimer: ####
Sections of this script not included in the API v1 documentations are not
supported, and may therefore not function properly in the foreseeable future--as
it may be the case with Azure ExpressRoute connectivity and enabling. 