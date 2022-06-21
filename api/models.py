from django.db import models , migrations

class Migration(migrations.Migration):
	atomic = False

# Create your models here.
class Users(models.Model):
	userId = models.TextField(primary_key=True)
	userName = models.CharField(max_length=200)
	passWord = models.CharField(max_length=200)
	avatar  = models.TextField()
	def __str__(self) -> str:
		return self.userName

class Categories(models.Model):
	categoryId = models.TextField(primary_key=True)
	categoryName = models.CharField(max_length=500)
	def __str__(self) -> str:
		return self.categoryName

class Post(models.Model):
	postId = models.TextField(primary_key=True)
	name = models.TextField()
	description = models.TextField()
	title = models.TextField()
	createAt = models.CharField(max_length=100)
	mainImg = models.TextField()
	categoryId = models.ForeignKey(Categories, on_delete=models.CASCADE )
	userId = models.ForeignKey(Users, on_delete=models.CASCADE)
	def __str__(self) -> str:
		return self.name

class Body(models.Model):
	bodyId = models.TextField(primary_key=True)
	content = models.TextField(blank=True)
	imageBody = models.TextField(blank=True)
	tittleBody = models.TextField(blank=True)
	postId = models.ForeignKey(Post, on_delete=models.CASCADE)
	def __str__(self) -> str:
		return self.tittleBody