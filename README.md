# OTUS LAB 1

Script dclnt.py make several actions:

* Load python code files from a certain repositories
* Get function names in python code files by using ast lib
* Search verbs in function names by using nltk lib
* Output most common verbs and it's occurence in a console

# Using script
Input some commands in a directory where dclnt.py located 

## Clone the certain repositories from github
```
$ git clone https://github.com/django/django.git
$ git clone https://github.com/pallets/flask.git
$ git clone https://github.com/Pylons/pyramid.git
```

## Create and activate virtual environment
```
$ python3 -m venv env
$ . env/bin/activate
``` 

## Install nltk library
```
$ pip install nltk
```

## Run script
```
$ python dclnt.py
```
See result of running proccess in a console 
