# Vlan Assignment Webex Teams Bot (Powered by Cisco DNA Center)
#### Assign switchport interfaces to access vlans using Webex Teams.
Quite a few IT organizations are still working with traditional L2/L3 networks without a NAC solution (e.g. Cisco ISE) providing automated Vlan allocation for each and every interfaces.
Those customers' networking teams spend their time associating switch ports to requested Vlans in a manual, time consuming manner. As vlan association required administrative privileges on the network switches - there is a risk offloading the task to the IT helpdesk. Moreover, the simple vlan association command still requires the network engineer to sit in front of their computer.
Using Cisco DNA Center's Intent API, we are able to provide:
1. An easy to use Webex Teams bot that will allow network engineers to change switch ports' associated vlan from anywhere (using their smartphone or any device capable of accessing Webex Teams).
2. An option to offload the repetitive task to less experienced teams, as the bot cannot make any change except associating vlans.

## Demo

1. Show switches:
<p align="center"><img src="img/Show_switches.gif"></p>

2. Show list of ports of a selected switch:
<p align="center"><img src="img/Show_ports.gif"></p>

3. Assign a port to a vlan:
<p align="center"><img src="img/Assign_ports.gif"></p>

## How to setup
### Python Webhook Listener
#### Prerequisites
* Docker support (optional)
* ngrok, for receiving the webhook notifications
* Cisco Webex Teams Token and Teams ID
	- How-To Guide https://developer.webex.com/docs/api/getting-started

### Start Python Webhook Listener
```
docker run -d -p 5000:5000 -e WEBEX_TEAMS_TOKEN="TOKEN" obrigg/cisco-dnac-port-association
```
### Cisco DNA-C
#### Prerequisites
* Enable Cisco DNA-C as a Platform. [How-To Guide](https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/dna-center-platform/1-3-3-0/user_guide/b_dnac_platform_ug_1_3_3_0/b_dnac_platform_ug_1_3_3_0_chapter_010.html)
