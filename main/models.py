from django.db import models
from django.contrib.auth.models import User

# Create your models here.
  
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    address = models.CharField(max_length=100, null=True, blank=True,default='')   
    pin_code = models.CharField(max_length=10, null=True, blank=True,default='')
    mobile_number = models.CharField(max_length=15, null=True, blank=True,default='')
    
    def __str__(self):
        return self.name
  
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    

    
class Polls(models.Model):
    question = models.CharField(max_length=200)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    def __str__(self):
        return self.question
    

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Polls, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    def __str__(self):
        return self.answer