from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import md5
import datetime
import os, binascii
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile('^[A-z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = []

        if len(postData['name']) < 2:
            errors.append("Name should be more than 2 characters")
        elif not NAME_REGEX.match(postData['name']):
            errors.append("Invalid letter")
        if len(postData['email']) < 2:
            errors.append("Email should be more than 2 characters")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Email invalid")
        if len(postData['password']) < 8:
            errors.append("Password should be more than 10 characters")
        elif postData['password'] != postData['password_confirm']:
            errors.append("Password is not matched")
        if len(postData['birthday']) < 0:
            errors.append("Please input your birthday")
            
#if there's no error then password 
        if len(errors) == 0 :
             # if email is found in db
            salt = binascii.b2a_hex(os.urandom(15)) 
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
             # add to database
            User.objects.create(name=postData['name'], email=postData['email'], birthday=postData['birthday'], salt=salt, password=hashed_pw)

        return errors

    def login(self, postData):
        errors = []
        # if email is found in db
        if User.objects.filter(email=postData['email']):
            salt = User.objects.get(email=postData['email']).salt
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
            # compare hashed passwords
            if User.objects.get(email=postData['email']).password != hashed_pw:
                errors.append('Incorrect password')
        # else if email is not found in db
        else:
            errors.append('Email has not been registered')
        return errors



class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateTimeField(auto_now=False, auto_now_add=False)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "user object: ---,{} ----{}, ----{}".format(self.name, self.email, self.birthday)

class ApptManager(models.Manager):
    def t_validator(self, postData):
        errors_t = {}
        if len(postData['tasks']) < 1:
            errors_t["tasks should not be empty!"] ="tasks should not be empty!"
        if (postData['date'] < str(datetime.date.today())):
            errors_t['date should be future-dated or current or today'] = 'date should be future-dated'
        # if len(postData['time'])< 3 :
        #     errors_t['time hould not be before the the current time'] = "Time should not be before the the current time"

        return errors_t 
        
 
class Appt(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    time = models.TimeField()
    tasks = models.CharField(max_length=255)
    status = models.CharField(max_length = 7)
    user = models.ForeignKey(User, related_name="upload_q")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ApptManager()
    def __repr__(self):
        return "object: {}, {}, {},{}".format(self.date,self.time, self.tasks)
