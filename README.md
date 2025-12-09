In this project we will create a web page API to interact with the Minecraft server (mac mini). Web API will be created in Flask. We will use macOS as a host and will use a container (Docker) to deploy webpage and Minecraft server. Overtime we will maintain this API for future use and develop more features.



DHCP (Dynamic Host Configuration Protocol) (Providing multiple IP addresses)

DNS (Domain name system, translating domain names to IP addresses)



API

* List available servers
* List players in server
* Server Options

Minecraft Server Options

* Map Selection 
* Difficulty
* Game Mode
* XP
* Summon 
* Reload
* Stop

**Phase I (HTML/CSS Template Creation)**

Notes:
* Install Flask (must have pip module on python first)
  * pip install Flask
* Creating a virtual Environment
  * python3 -m virtualenv .venv
* Run the virtual Envirnment (Make sure .env folder is created)
  * .\.venv\Scripts\activate (Use unmodded Powershell for windows)
* Run python_flask application
  * py -m flask --app 'python_file.py' run

**Phase II (Script Programming)**

Brainstorm:
* Securty when accessing secure shells on each servers. (need ssh keys)
  * Having macOS accept ssh keys might be challenging
* Create a script to read the following
  * Does IP Address reach server?
  * What architecture and OS?
  * Does the environment has the minecraft server file?
  * Is java installed?

* Contents of containers for servers:
  * python
  * java
  * minecraft server
  * scripts (if neccessary)

**Phase III (Web and Server Interaction)**

**Aditional Notes:**
* We need to have a python installer folder for spectific architecture (ARM64,Win,OSX) for container usage.

