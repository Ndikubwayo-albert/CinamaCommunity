from django.db import models
from django.contrib.auth.models import User
from PIL import Image



class CreateUser(models.Model):
    gender = (("Male", 'M'),
              ("Female", 'F'),
              ("Others", 'O')
              )
    user_uuid = models.CharField(max_length=250, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    user_gender = models.CharField(max_length=15,choices=gender)
    email_token = models.CharField(max_length=250)
    avatar = models.ImageField(default='default.png', upload_to='profiles')
    is_verfied = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.user.username} {self.user_uuid}'

    # def save(self, *args, **kwargs):
    #     super(CreateUser, self).save(*args, **kwargs)

    #     img = Image.open(self.avatar.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.avatar.path) 
    
class Contactus(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField(max_length=1000)
    
    def __str__(self):
        return self.name 
    
class AddPost(models.Model):
    user_uuid = models.ForeignKey(CreateUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    release_date = models.DateField()
    main_actors = models.TextField() 
    genre = models.TextField()
    description = models.TextField()
    poster = models.ImageField(default='poster.png', upload_to='posters')
    movie_trailer = models.CharField(max_length=250, default="www.youtube.com") 
    posted_time = models.DateTimeField()
    

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     super(AddPost, self).save(*args, **kwargs)

    #     img = Image.open(self.poster.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.poster.path) 
     
    

class Comment(models.Model):
    user_uuid = models.ForeignKey(CreateUser, on_delete=models.CASCADE)
    post = models.IntegerField()
    message = models.TextField()
    posted = models.DateTimeField()

    def __str__(self):
        return self.message
    