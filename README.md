# Majirani
-------------------------------
## Description

 A Django web application informing users about everything happening in their neighborhood


------------------------------------------------------------------------
## BY: Tony Kihara

![image]("https://z-p3-scontent.fmba2-1.fna.fbcdn.net/v/t1.0-1/c17.0.100.100a/p100x100/47320452_529937297486237_2233373106905284608_n.jpg?_nc_cat=108&_nc_oc=AQnOOcLzauYHmw617fKkKBFbwp3BR7Kr4fdkVXILLphT9_TcZwg0uxj6oF4HhozJDmk&_nc_ht=z-p3-scontent.fmba2-1.fna&oh=a8fd90a26d02a55397b10abe1426f925&oe=5DDEBE7B")

-----------------------------------------
## BDD
|Behaviour|Input|Output|
|:----|:-----|:-------|
|Create an account|By clicking the sign up button and entering the needed details|One is able to log in meaning he/she would have created an account|
|Create a neigbourhood|After one clicks the create hood button and enters the needed details|Other users are able to see and even join if they are intersted in your neighbourhood|
|Join a neigbourhood|One sees a number of neigbourhood and thus when he/she clicks to join one and enters the needed details |Then he/she will have been added in the neighbourhood and can participate in it|

------------------------------------------------------------
## User Requirements

+ [x] Sign in with the application to start using.
+ [x] Set up a profile about me and a general location and my neighborhood name.
+ [x] Find a list of different businesses in my neighborhood.
+ [x] Find Contact Information for the health department and Police authorities near my neighborhood.
+ [x] Create Posts that will be visible to everyone in my neighborhood.
+ [x] Change My neighborhood when I decide to move out.
+ [x] Only view details of a single neighborhood.

-----------------------------------------------------------
## Admin Dashboard
~~~
 Use django admin to post photos to the database and manage the photos
~~~

-------------------------------------------
## Setup

### Requirements
This project was created on a debian linux platform but should work on other unix based[not limited to] sytems.
* Tested on Debian Linux
* Python3

### Cloning the repository
```bash
git clone https://github.com/Kihara-tony/Majirani && cd Majirani
```

### Creating a virtual environment

```bash
python3 -m virtualenv virtual
source virtual/bin/activate
```
### Installing dependencies
```bash
pip install -r requirements.txt
```

### Prepare environmet variables
Create a .env file and add the following configutions to it
```python
SECRET_KEY= #secret key will be added by default
DEBUG= #set to false in production
DB_NAME= #database name
DB_USER= #database user
DB_PASSWORD=#database password
DB_HOST="127.0.0.1"
MODE= # dev or prod , set to prod during production
ALLOWED_HOSTS='.herokuapp.com',
```

### Database migrations

```bash
python manage.py migrate
```

### Running Tests
```bash
python manage.py test
```

### Running the server 
```bash
python manage.py runserver
```

------------------------------------------------
## Contributing

- Git clone [https://github.com/Kihara-tony/Majirani](https://github.com/Kihara-tony/Majirani) 
- Make the changes.
- Write your tests.
- If everything is OK. push your changes and make a pull request.

### Deploying to heroku
Refer to this guide: [deploying to heroku](https://simpleisbetterthancomplex.com/tutorial/2016/08/09/how-to-deploy-django-applications-on-heroku.html)
Set the configuration to production mode

-------------------------------------
## Live Demo

The web app can be accessed from the following link: 
[Majirani](https://majirani.herokuapp.com/)

---------------------------------
## Technology used

* [Python3.6](https://www.python.org/)
* [Django 1.11](https://docs.djangoproject.com/en/1.11/)
* [Heroku](https://heroku.com)
* [PostrgeSql]
* [Bootstrap 3]

----------------------------------------------
## License
MIT License

Copyright(c) 2019 Tony Kihara Njenga

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from django.conf import settingsfrom django.conf import settings