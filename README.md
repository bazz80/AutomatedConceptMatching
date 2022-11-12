# AutomatedConceptMatching

**Initial Setup and Configuration**

Import the supplied OVF file into either VMware Workstation/Player or VMware ESXi by following the procedure from VMware:
<br>VMware Workstation or Player
<br>https://docs.vmware.com/en/VMware-Workstation-Player-for-Windows/16.0/com.vmware.player.win.using.doc/GUID-DDCBE9C0-0EC9-4D09-8042-18436DA62F7A.html
<br>VMware ESXi
<br>https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.hostclient.doc/GUID-8ABDB2E1-DDBF-40E3-8ED6-DC857783E3E3.html

Configure VM network as per your local environment, either in Bridged mode or Nat for VMware Workstation; VMware ESXi configure VM Network to be on one with DHCP.

Open VM remote console, login with the following credentials:
User: mimosa
Passwprd: HELPplcs22

Run ifconfig to find the current IP Address.

SSH using same credentials.

Change directory to:
/home/mimosa/AutomatedConceptMatching

Cat config.ini to view current Thresholds and Weighting. SQL Server Configuration shouldn't require changing.
If Thresholds or Weighting need to be changed:
VIM config.ini and make the required changes.
mySQL Server credentials:
user: matches
password: HELP!plcs22


To run a new analysis, drop existing data from the database and repopulate,
Run
python3 main.py

For CLI view of Concept Matches:
Run
python3 show_matches.py

For GUI view, browse to the IP address assigned via DHCP.
