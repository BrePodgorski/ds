from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self,data):
        errors=[]
        if data['f_name']=="":
            errors.append("First name cannot be left blank.")
        if len(data['f_name'])<2:
            errors.append("First name cannot be less than two characters long.")
        if data['l_name']=="":
            errors.append("Last name cannot be left blank.")
        if len(data['l_name'])<2:
            errors.append("Last name cannot be less than two characters long.")
        if not data['f_name'].isalpha():
            errors.append("First name can only accept letters.")
        if not data['l_name'].isalpha():
            errors.append("Last name can only accept letters.")
        if len(data['email'])<1:
            errors.append("Email cannot be left blank.")
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Please enter a valid email.")
        if len(data['password'])<8:
            errors.append("Your password must be at least 8 characters long.")
        if not data['password']==data['conf_password']:
            errors.append("Your passwords must match.")
        try:
            User.objects.get(email=data['email'])
            errors.append("You already have an account! Please Login.")
        except:
            pass
        if len(errors)==0:
            user=User.objects.create(f_name=data['f_name'], l_name=data['l_name'], email=data['email'], password=bcrypt.hashpw(data['password'].encode(),bcrypt.gensalt()))
#refferring to user HERE
            print id
            return {'user':user, 'errors':None}
        else:
            return {'user':None, 'errors':errors}

    def login(self,data):
        errors=[]
        try:
            user=User.objects.get(email=data['email'])
            if bcrypt.hashpw(data['password'].encode(),user.password.encode())!= user.password.encode():
                errors.append("Wrong password!")
        except:
            errors.append("You do not have an account, please register!")
        if len(errors)!=0:
            return {'user':None, 'errors':errors}
        else:
            return {'user':user, 'errors':None}

class User(models.Model):
    f_name=models.CharField(max_length=50)
    l_name=models.CharField(max_length=50)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=255)
    objects=UserManager()


class Secret(models.Model):
    secret=models.CharField(max_length=30)
    user=models.ForeignKey(User, related_name="user_secret")
    created_at=models.DateTimeField(auto_now_add=True)
    objects=UserManager()

class Like(models.Model):
    user=models.ForeignKey(User, related_name='user_likes')
    # To know which user is liking what. Many users can like many secrets.
    secret=models.ForeignKey(Secret, related_name='secret_likes')
    # To know what secret is being liked
    objects=UserManager()
