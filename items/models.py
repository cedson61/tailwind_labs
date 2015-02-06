from django.db import models
from django.core.urlresolvers import reverse

class TimeStampedModel(models.Model):
    """An abstract base class for timestamp fields, which can
       then be added to any model (DRY!)"""
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    """Custom model manager, to return only active items."""
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True)


class Item(TimeStampedModel):
    # since we subclass the ABC above, we also get created and modified attributes.
    """Just a silly example model for demo purposes."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    url = models.URLField(blank=True)

    # per 2 scoops, always do this before defining a custom manager.
    # among other reasons, it is necessary in order to show both active and 
    # inactive items in the admin.
    objects = models.Manager() 

    active = ActiveManager()   # used in the app to return only active Items

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-modified']

    def get_absolute_url(self):
        return reverse('items:item_detail', kwargs={'pk': self.pk})