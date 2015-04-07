# project-wildfire
Backend Django server for Wildfire


##Installation

####Requirements
This project assumes that the following are already installed:  

- Python ver 2.7.X
- pip ver 6.0 
- PostgreSQL ver 9.3


####Installation
To install, first clone the repo (or unzip the folder):

	https://github.com/jordanbang/project-wildfire.git

Then, change into the directory and install the requirements:

	cd project-wildfire
	pip install -r requirements.txt
	
This will install the required Python packages used within the project.

Then, got to the hellodjango directory, and edit the databases section of the settings file to contain your database information.  Specifically, you will need to change the user field and password field.  If the database is not being run locally, then that information will need to change as well.

	DATABASES = {
    	'default': {
        	'ENGINE': 	'django.db.backends.postgresql_psycopg2',
        	'NAME': 'mysite',
	        'USER': '(your username)',
    	    'PASSWORD': '(your password)',
       		'HOST': '127.0.0.1',
    	    'PORT': '5432',
	    }
	}
	
Once the database information is correct, migrate the database schema and run the Django application:

	python manage.py migrate
	python manage.py runserver
	
This will start the server on localhost, port 8000.

The API can now be queried using CURL or a browser, by hitting any of the provided endpoints, such as:
	
	http://127.0.0.1:8000/wildfire/question/
