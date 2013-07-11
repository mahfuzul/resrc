# coding: utf-8

from hashlib import md5

from django.db import models
from django.contrib.auth.models import User

from resrc.link.models import Link
from resrc.list.models import List


class Profile(models.Model):
    '''User profile'''
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    user = models.ForeignKey(User, unique=True, verbose_name='user')

    avatar_url = models.CharField('avatar URL', max_length=128, null=True, blank=True)

    about = models.TextField('about', blank=True)

    karma = models.IntegerField('karma', null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return '/u/user/{0}'.format(self.user.username)

    def get_avatar_url(self):
        if self.avatar_url:
            return self.avatar_url
        else:
            return 'http://gravatar.com/avatar/{0}?d=identicon'.format(md5(self.user.email).hexdigest())

    def get_link_count(self):
        return Link.objects.all().filter(author__pk=self.user.pk).count()

    def get_list_count(self):
        return List.objects.all().filter(author=self.user).count()

    # Links

    def get_links(self):
        return Link.objects.all().filter(author=self.user)

    # Lists

    def get_lists(self):
        return List.objects.filter(authors=self.user.pk)

    def get_public_lists(self):
        return self.get_lists().filter(is_public=True)

    def get_private_lists(self):
        return self.get_tutorials().filter(is_public=False)