from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save

from django.dispatch import receiver


# Create your models here.

class Neighbourhood(models.Model):
    """
    class for creating neighbourhood
    """
    name = models.CharField(max_length=2000)
    location = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='media/', null=True)
    description = models.CharField(max_length=10000, null=True)
    police = models.IntegerField(null=True)
    Hospital = models.IntegerField(null=True)
    admin = models.ForeignKey('Profile', related_name='Neighbourhood', null=True)

    def __str__(self):
        return self.name

    def create_neighbourhood(self):
        """
        method to save project images
        :return:
        """
        self.save()

    @classmethod
    def find_neighbourhood(cls, neighbourhood_id):
        """
        method to get image by id
        :return:
        """
        neighbourhood = cls.objects.filter(id=neighbourhood_id)
        return neighbourhood

    @classmethod
    def update_neighbourhood(cls):
        """
        method to update neighbourhood details
        :return:
        """
        info = cls.objects.all().update()
        info.save()
        return info

    def delete_neighbourhood(self):
        """
        method to delete image
        :return:
        """
        self.delete()

    @classmethod
    def search_business_hood(cls, search_term):
        """
        method to search for business by neighbourhood
        :return:
        """
        business = cls.objects.filter(biz__name__icontains=search_term)
        return business


class Profile(models.Model):
    """
    class for user profile
    """
    avatar = models.ImageField(upload_to='media/', null=True)
    name = models.CharField(max_length=2000)
    bio = models.CharField(max_length=2000, null=True)
    email = models.CharField(max_length=2000)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE,  null=True)

    def __str__(self):
        return self.user.username

    # sender is source of signal
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        """
        method to create profile
        :return:
        """
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance,saved, **kwargs):
        """
        method to save profile
        :return:
        """
        if saved:
            Profile.objects.save(user=instance)


class Business(models.Model):
    """
    class for creating businesses
    """
    name = models.CharField(max_length=2000)
    email = models.CharField(max_length=2000)
    number = models.IntegerField(null=True)
    description = models.CharField(max_length=15000, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='business', null=True)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, related_name='business', null=True)

    def __str__(self):
        return self.name

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    @classmethod
    def find_business(cls, search_biz):
        """
        method to find business by id
        :param business_id:
        :return:
        """
        business = cls.objects.filter(name=search_biz)
        return business

    @classmethod
    def update_business(cls):
        """
        method to update business details
        :return:
        """
        biz = cls.objects.all().update()
        biz.save()
        return biz


class Post(models.Model):
    """
    class for creating posts
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post')
    content = models.TextField()
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, related_name='post', null=True)

    def save_post(self):
        self.save()


class Comment(models.Model):
    """
    class for creating comments on posts
    """
    comment = models.CharField(max_length=10000, null=True)
    post = models.ForeignKey(Post, related_name='comment', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment", null=True)

    def save_comment(self):
        self.save()