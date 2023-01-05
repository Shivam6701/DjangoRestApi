from enum import auto
from typing import Optional
import django
from django.db import models
from sqlalchemy.orm import relationship

class Post(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    content = models.CharField(max_length=200,blank=False, default='')
    published = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    owner_id=models.ForeignKey("User", on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return self.title


class User(models.Model):
    username=models.CharField(max_length=20, blank=False,unique=True,default='')
    name=models.CharField(max_length=30,blank=False,default='')
    password=models.CharField(max_length=200,blank=False,default='')
    email = models.EmailField(max_length=30, blank=False,unique=True,default='')
    created_at=models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.name
        


