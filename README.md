# Atrade-Stock-Exchange-Web-Application
A Stock Market Project created with 3 different servers with many features such as caching, authentication, security etc.

Technologies Used:
	- Django Framework in all three Servers
	- MySQL Database
	- Google OAuth Single Sign On
	- Memcached for data caching
	- User tokens for authorising web services access.
	- External API Integration for realtime stock exchange data.


Basic Setup
Server 01.
	- It is django project, hence set up a django environment and copy the project files into it.
	- required python modules:
		- Django
		- numpy
		- requests
		- json
		- cors middleware
	- After copying th files, open Project/project/settings.py and set up email details, set up templates path in your system.
	- Create your Google SSO client Key and add it to head tag in server 01	
	- Change paths to server 2 requests in atrades1/views.py and all templates that are making calls to server 02.
	- Server is ready to run

Server 02
	- It is django project, hence set up a django environment and copy the project files into it.
	- required python modules:
		- Django
		- numpy
		- requests
		- json
		- cors middleware
		- rest framework
		- mysql_client
		- memcached
	- Set up MySQL Server connection in settings.py
	- Change paths to server 3 requests in atrades2/views.py and all templates that are making calls to server 03.
	- Server is ready to run

Server 03
	- It is django project, hence set up a django environment and copy the project files into it.
	- required python modules:
		- Django
		- random
		- requests
		- json
		- datetime
	- server is ready to run

Important Notes:
	- In future, the key provided by google for single signon might expire, hence it will be better that while setting up this project, you create your own authentication key and then set up the project.
	- The email id and password setup must be done to make reset password functionality work.
	- It is also necessary that you create your own AlphaVantage API key from the website, it is free and use that key in server 03 for seemless experience.
