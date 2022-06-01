from django.db import models

# Create your models here.
class FaqsModel(models.Model):
   
    question = models.TextField(max_length = 1000, default = '')
    answer = models.TextField(max_length = 1000, default = '')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # done 
    def __str__(self):
        return f'{self.question}'
