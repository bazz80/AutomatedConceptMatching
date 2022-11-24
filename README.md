# AutomatedConceptMatching
AutomatedConceptMatching is a script that automates the comparison of concepts found in the MIMOSA Standard and ISO 10303-239 PLCS Standard. The script delivers the matches score, their description, name and relationships through the use of FuzzyWuzzy, to a database store. The database can be accessed through the provided web interface hosted in Azure cloud, so that users can view, search and interact with the results. 

<h2>Initial Setup and Configuration for Azure</h2>
<h3>Azure Database for MySQL flexible server</h3>
Create an instance of Azure Database for MySQL flexible server in your resource group and preferred region.<br>

Configure credentials during instance creation and take note of these.<br>
The demo one has the following credentials used:<br>
Administrator: matches<br>
Password: HELP!plcs22<br>
Add any other MySQL Client IP addresses (such as office or home for testing)<br>
Tick checkbox "Allow public access from any Azure service within Azure to this server"<br>
<br>
Once deployed, create a new database of name "automatedmatching"<br>

<h3>Azure Web App - To run the python code</h3>
Create new Azure Web App:<br>
Basics:<br>
Publish: Code<br>
Runtime Stack: Python 3.10<br>
Operating System: Linux<br>
<br>
Deployment:<br>
Configure to be a cloned source of thie Git repository, using the Azure branch<br>
SSH and edit the main.py or config.ini to include the MySQL credentials and server name<br>
If there are issues with running the code due to dependencies not installed during deployment, may need to run the following:<br>
pip install bs4 sqlalchemy BeautifulSoup4 pandas fuzz fuzzywuzzy configparser python-Levenshtein pymysql html5lib lxml<br>
<br>
Done. :)<br>
https://github.com/bazz80/AutomatedConceptMatching_WebApp<br>
<br>


<h2>Setup Automated Matching Script</h2>
The automated matching script is contained in the main.py file. The program contains a config.ini file where you will need to add your SQL server information.
To generate this, please run the program once. You will then be able to populate the config.ini file with the following options.


[THRESHOLDANDWEIGHTING]

threshold = 40

name weighting = 65

description weighting = 23

relationship weighting = 12


[SQLSERVERCONFIG]

user = root

password = password1

database = automatedmatching


<h3>Threshold and Weighting</h3>

Please ensure you have entered a threshold between 0 and 100. This will determine what the minimum similarity score shown to you will be.

To determine the weighting of the name, description and relationship similarity values please enter a combination of numbers that total 100%.

It is important that the database you enter in the config.ini file is the same database you will be using to connect to the web interface.


<h2>Display Results of Matches</h2>
To run a new analysis, drop existing data from the database and repopulate,
<br>Run:
<br>python3 main.py
<br>
For CLI view of Concept Matches,
<br>Run:
<br>python3 show_matches.py


