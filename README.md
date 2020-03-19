# vraDNS-action
Create a ZIP package for Python runtime extensibility actions including propietary Python libraries

You can create a ZIP package that contains the Python script and dependencies used by your vRealize Automation Cloud Assembly extensibility actions.

There are two methods of building the script for your extensibility actions:

Writing your script directly in the extensibility action editor in vRealize Automation Cloud Assembly.
Creating your script on your local environment and adding it, with any relevant dependencies, to a ZIP package.
By using a ZIP package, you can create a custom preconfigured template of action scripts and dependencies that you can import to vRealize Automation Cloud Assembly for use in extensibility actions.

Furthermore, you can use a ZIP package in scenarios where modules associated with dependencies in your action script cannot be resolved by the vRealize Automation Cloud Assembly service, such as when your environment lacks Internet access.

You can also use a ZIP package to create extensibility actions that contain multiple Python script files. Using multiple script files can be useful for organizing the structure of your extensibility action code.

# Requirements
    vRA 8.X or vRA Cloud with ABX or Azure FaaS or AWS Lambda and associated configured Cloud Accounts
    Ubuntu 18.04.4 LTS
    Python 3.6.9
    pip 9.0.1
    dnspython==1.16.0

    * Please note that the runtime of action-based extensibility in vRealize Automation Cloud Assembly is Linux-based.
    Therefore, any Python dependencies compiled in a Windows environment might make the generated ZIP package unusable for the creation of extensibility actions. Therefore, you must use a Linux shell.

# Install Python 3

Ubuntu 18.04 ships with both Python 3 and Python 2 pre-installed. To make sure that our versions are up-to-date, let’s update and upgrade the system with the apt command to work with Ubuntu’s Advanced Packaging Tool:

	sudo apt update
	sudo apt -y upgrade
	
check the version of Python 3 that is installed in the system by typing:

	python3 -V

Output
	Python 3.6.5

To manage software packages for Python, let’s install pip, a tool that will install and manage programming packages like the requirements for our ABX Action

	sudo apt install -y python3-pip

# Create and activate a new Python environment:

	root@ubuntu_server: mkdir environments
	root@ubuntu_server: python3 -m vraDNSDev --> It creates an activates a python3 development environment
	(vraDNSDev) root@ubuntu_server: mkdir vraDNS-action     --> This is the root folder for your action
	(vraDNSDev) root@ubuntu_server: cd ~/enviroments/vraDNSDev/vraDNS-action

# Define your library requirements and install them with PIP at your action root folder

	(vraDNSDev) root@ubuntu_server: vi requirements.txt --> place this file inside your action root folder 
		dnspython==1.16.0    --> This is me only propetary library that I need and that it is not included at the standard Python
	(vraDNSDev) root@ubuntu_server:  pip install -r requirements.txt --target=/root/enviroments/vraDNSDev/vraDNS-action   --> Install dnspython in my virtual enviroment

You should see the following folders:

	(vraDNSDev) root@ubuntu_server:~/enviroments/vraDNSDev/vraDNS-action# ls -lrt
	total 408
	drwxr-xr-x 4 root root   4096 Mar  3 01:00 dns
	drwxr-xr-x 2 root root   4096 Mar  3 01:00 dnspython-1.16.0.dist-info
	-rw-r--r-- 1 root root    759 Mar  3 17:21 main.py
	-rw-r--r-- 1 root root     18 Mar  3 17:46 requirements.txt

My principal and only Python Script is "main.py"
It is a basic sample for translating a MSISDN number into ENUM format calling dnspython's dns.e164.from_e164()
it also resolves and lists the MX records for a given domain via dnspython's dns.resolver.query()
and finally resolve A record with prebuilt python's socket library

	/////////main.py////////
	import socket
	import dns.resolver
	import dns.e164

	def handler(context, inputs):
	    print('Action started.')
	    msAddr = inputs["msisdn"]
	    dnsMX = inputs["dnsMX"]

	    # Log Input Entries
	    #print (inputs)
	    #print (msAddr)
	    #print (dnsMX)

	    # Converts E164 Address to ENUM with propietary library dnspython
	    n = dns.e164.from_e164(msAddr)
	    print ('My MSISDN:', dns.e164.to_e164(n), 'ENUM NAME Conversion:', n)

	    # Resolve DNS MX Query with propietary library dnspython
	    answers = dns.resolver.query(dnsMX, 'MX')
	    print ('Resolving MX Records for:', dnsMX)
	    for rdata in answers:
		print ('Host', rdata.exchange, 'has preference', rdata.preference)

	    # Resolve AAA with prebuilt socket library
	    addr1 = socket.gethostbyname(dnsMX)
	    print('Resolving AAA Record:', addr1)

	    return addr1
	//////////////////

Package the main Script with the installed libraries
Both your script and dependency elements must be stored at the root level of the ZIP package. When creating the ZIP package in a Linux environment, you might encounter a problem where the package content is not stored at the root level. If you encounter this problem, create the package by running the zip -r command in your command-line shell.

	(vraDNSDev) root@ubuntu_server: cd ~/enviroments/vraDNSDev/vraDNS-action
	(vraDNSDev) root@ubuntu_server: zip -r9 vraDNS-actionR08.zip *

Let's use the ZIP package to create an extensibility action script by importing it at vRA
Log In to vRA with a user having Cloud Assembly Permissions
Create a New Action

    <INSERT NEW ACTION IMAGE>

Select Import and pick up your zip file (e.g. vraDNS-actionR08.zip is a pre-staged working action) 

    <INSERT IMPORT IMAGE>

Define inputs required by the script ( see defaults below ) and define the Main Function as point of entry 

    <INSERT INPUT IMAGE>

Please note that for actions imported from a ZIP package, the main function must also include the name of the script file that contains the entry point. For example, if your main script file is titled main.py and your entry point is handler (context, inputs), the name of the main function must be main.handler.

You can select your prefered FaaS Provider

Save and Test your ABX Action

  <INSERT INPUT IMAGE>

You can change the input ( please note that the MSISDN is in international format and dnsMX don't need WWW as it is an EMAIL Exchange Record)

    <INSERT INPUT IMAGE>

From this point you could create an Extensibility Subscrition or expose this action at vRA's Service Broker Catalog

Don't forget to deactivate your Python enviroment

	(vraDNSDev) root@ubuntu_server:~/enviroments# deactivate
	root@ubuntu_server:~/enviroments#
