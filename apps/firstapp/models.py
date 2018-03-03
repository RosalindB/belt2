# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re, bcrypt
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def createUser(self, postData):
        result = {
            'status' : True,
        }
        errors = []

        if len(postData['my_name']) < 3:
            errors.append('Name needs to be longer than 3 characters.')

        if len(postData['pw']) < 8:
            errors.append('Password is too short.')

        if postData['pw'] != postData['cpw']:
            errors.append("Passwords don't match")
        
        if len(self.filter(email=postData['email']))>0:
            errors.append('Email already in use. Please use a different email.')
        
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("You must submit a valid email.")
    
        if len(errors) > 0:
            result['status'] = False
            result['errors'] = errors  

        else:
            user = User.objects.create(
                my_name=postData['my_name'],
                alias=postData['alias'],
                email=postData['email'],
                dob=postData['dob'],
                password=bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt()))
            result['user'] = user
        return result
    
    def login_validation(self, postData):
        response = {
            'status' : True
        }
        errors = []

        user = User.objects.filter(email = postData['email'])

        if len(user) > 0:   # query set was not empty - i.e. there was a user
        # check this user's password
            user = user[0]
            if not bcrypt.checkpw(postData['pw'].encode(), user.password.encode()):
                errors.append('password is incorrect')
        else:
            errors.append('email does not exist - please register')

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            response['user'] = user
        return response
        
        
class User(models.Model):
    id = models.AutoField(primary_key=True)
    my_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    favorited_by = models.ManyToManyField('Quotes', related_name="favorites", default=None)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __str__(self):
        return 'alias: {}, id:{}'.format(self.alias, self.id)  

class Quotes(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    quote_by = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='quote')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()

    def __str__(self):
        return 'user: {}, id:{},'.format(self.author, self.id) 

