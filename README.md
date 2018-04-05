# Installation Information

**In order to run FSJAwards, you will need to install the software required by this program. Installation instructions are as follows.**

#### Step 1) Install Python
Install Python3 with <br>
`sudo apt-get install python3` <br>
or install Python 2.7 with <br>
`sudo apt-get install python`

#### Step 2) Install Pip
Install Pip for Python3 with <br>
`sudo apt install python3-pip` <br>
or Python 2.7 with <br>
`sudo apt install python-pip`

#### Step 3) Install Django Filters
Install Django Filters for Python3 with <br>
`pip3 install django-filter` <br>
or for Python 2.7 with <br>
`pip install django-filter`

#### Step 4) Install Widget Tweaks
Install Widget Tweaks for Python3 with <br>
`pip3 install django-widget-tweaks` <br>
or for Python 2.7 with <br>
`pip install django-widget-tweaks`

<br>

# Deployment Information

**In order to deploy FSJAwards on a local or remote machine, please follow the steps below**

#### Step 1) Make migrations
Use the included manage.py file to create a migration for the relational database. Navigate to the folder containing manage.py and run the following command from the terminal <br>
`python3 manage.py makemigrations` <br>
or if you are using Python 2.7, run <br>
`python manage.py makemigrations`

#### Step 2) Migrate
Migrate the changes you made with the following command <br>
`python3 manage.py migrate` <br>
or if you are using Python 2.7, run <br>
`python manage.py migrate`

#### Step 3) Create a superuser
Create a superuser account for the site with the following command <br>
`python3 manage.py createsuperuser` <br>
or if you are using Python 2.7, run <br>
`python manage.py createsuperuser` <br>
and follow the onscreen prompts to create a superuser account

#### Step 4) Start the server
Start the server with the following command <br>
`python3 manage.py runserver` <br>
or if you are using Python 2.7, run <br>
`python manage.py runserver`
