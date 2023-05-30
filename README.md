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

# link to documentation of API v1
--> https://help.skytap.com/API_Documentation.html#top

# blurb on where it can be run--Azure account using cloudShell
--> upload script from file: https://learn.microsoft.com/en-us/azure/cloud-shell/persisting-shell-storage#upload-files