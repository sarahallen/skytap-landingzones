# Skytap Landing Zones #
Get started with Skytap Environment creation using the Rest API. This script is a template that, when edited to include user-specific credentials and variables, will:

- Create a new environment within a Skytap account.
- Create two LPARs/VMs within the environment. 
- Configure the environment's network.
- Establish a connection with an Existing Azure ExpressRoute.
- Connect the newly created Skytap environment nextwork to the ExpressRoute.

## Pre-Requisites: ##
* An active Skytap account or Skytap on Azure services. 
* Skytap account email address or Skytap on Azure auto-generated email address. 
* Skytap REST API key or Skytap account password.
  [Link Text](https://help.skytap.com/kb-generate-api-token.html)
* An active Azure ExpressRoute service key. Follow Skytap's documentation for created a customer-managed ExpressRoute in Azure: [Link Text](https://help.skytap.com/wan-create-self-managed-expressroute.html)
* May need to install `requests` library.

## How to run this script ##
Set up your Azure ExpressRoute prior to running this script. You can utilize your 
Azure portal or the following Azure Networking scripts on GitHub: 
https://github.com/poomnupong/azure-networking.git

You can clone this repo, save it to your machine, 
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
    
#### Public Templates:
Skytap provides public templates for customer use. Various operating systems and versions are available, and can be found in a Skytap account under 'Templates':
[Link Text](https://help.skytap.com/using-public-templates.html)

This script uses Template IDs for environment and VM creation. Here is a reference for a few common templates used in customer environments:

| Template    | ID | 
| -------- | ------- |
| Windows Server 2022 Standard Sysprepped  | 2111381    |
| IBM i 7.4 TR 5   | 2110325     |
| AIX - AIX7.3TL0SP1-2148    | 2125303   |
| Ubuntu 18.04.1 LTS Desktop Firstboot    | 2038279  |

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
Sections of this script not included in the API v1 documentation are not
supported, and may therefore not function properly in the foreseeable future––as
it may be the case with Azure ExpressRoute connectivity and enablement. 
