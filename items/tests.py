from django.test import TestCase
from .models import Item

class ItemMethodTests(TestCase):
    """An inactive item should not be viewable."""
    pass

    """Another user's items should not be visible to the current user"""