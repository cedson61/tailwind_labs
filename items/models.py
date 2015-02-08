from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """An abstract base class for timestamp fields, which can
       then be added to any model (DRY!)"""
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Item(TimeStampedModel):
    # since we subclass the ABC above, we also get created and modified attributes.
    """Just a silly example model for demo purposes."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    url = models.URLField(blank=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('items:item_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-modified']
