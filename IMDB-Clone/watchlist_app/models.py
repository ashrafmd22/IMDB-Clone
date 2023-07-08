from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User #ye user model django m by default hota h

#ham models m hi relationship establish krte h
class StreamPlatform(models.Model):
    
    name= models.CharField(max_length=30)
    about=models.CharField(max_length=150)
    website=models.URLField(max_length=100)
    def __str__(self):
        return self.name


class WatchList(models.Model):
    title= models.CharField(max_length=50)
    description= models.CharField(max_length=200)
    Platform=models.ForeignKey(StreamPlatform ,on_delete=models.CASCADE, related_name='watchlist') #stream 
    # platform ki key yaha likhdi ye many to one relationship
    # h one movie ek hi platform par hogi but ek platform par bht sari movies ho skti h
    #on delete se hoga ke agar platform delete hua to saari movies apne aap delete ho jaygi
    active= models.BooleanField(default='True')
    avg_rating= models.FloatField(default=0)
    number_rating= models.IntegerField(default=0)
    created= models.DateTimeField(auto_now_add=True) # jaise hi ham object create krenge apne aap 
    #uska time isme ajayga

    def __str__(self):
        return self.title
    
class Review(models.Model):
    review_user=models.ForeignKey(User,on_delete=models.CASCADE) #user table by default hota h 
# and user table and user  delete hote hi uske review bhi delete kr 
    rating= models.PositiveBigIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description= models.CharField(max_length=200,null=True)
    watchlist=models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name="reviews")
    active= models.BooleanField(default=True)# active represent krega review genuine h ya fake active true to genuine
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.rating) + "--" + self.watchlist.title + " | " + str(self.review_user)

