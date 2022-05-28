# DevKit - Developer's Tool Kit
#### This Web Tool Kit is design to help developers to quickly generate basic template of project by providing requirements.
#### Project Devloped by : Team PSU
**Tech Stack used**
  * Python
  * Django Framework
  * Sqlite Database
  * Bootstrap
  * PyYAML
  * BeautifulSoup

# DevKit Steps to RUN at LocalHost 

```bash
cd Devkit
```

## Installation
#### Create a virtual environment to install dependencies in and activate it:

```bash
Devkit> python -m venv venv
```
```bash
Devkit> venv\Scripts\activate.bat
```

#### Then install the dependencies:
```bash
(venv)Devkit>  pip install -r requirements.txt
```

Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.


#### Once pip has finished downloading the dependencies:
##### For applying migrations or to creating new migrations
  
```bash
(venv)Devkit>  python manage.py makemigrations
```
```bash
(venv)Devkit>  python manage.py migrate
```
Note: The above-mentioned commands are required at installation and also every time when changes are done in Django models (Database)


#### To runserver
```bash
(venv)Devkit>  python manage.py runserver
```

#### And navigate to http://127.0.0.1:8000/.


#### To create admin account
```bash
(venv)Devkit> python manage.py createsuperuser
```
Enter username, email & password

#### To access admin dashboard visit  http://127.0.0.1:8000/admin
