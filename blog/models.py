from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.


class Post(models.Model):
	author = models.ForeignKey('auth.User') # this will connect each post to its author (User is a class)
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date  =  models.DateTimeField(default=timezone.now())
	published_date = models.DateTimeField(blank=True,null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def get_absolute_url(self):     # once a published button is hit where to take the user we will take it to a
									# "post_detail" page 
		return reverse("post_detail",kwargs = {'pk': self.pk})

	def approve_comments(self):
		return self.comments.filter(approved_comment = True)

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey('blog.Post',related_name = 'comments')  # this line will connect each comment to its actual post
	author = models.CharField(max_length = 200)
	text = models.TextField()
	create_date = models.DateTimeField(default = timezone.now())
	approved_comment = models.BooleanField(default=True)   #"approved_comment" class data item must match with the approved_comment earlier(name)
	

	def approve(self):
		self.approved_comment =True
		self.save()


	def get_absolute_url(self):
		return reverse('post_list')  # we will send the comment poser back to the page where all the posts are present
	def __str__(self):
		self.text 


