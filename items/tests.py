from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser, User
from .models import Item
from .views import ItemListView


def create_item(user, id=1):
    return Item(id=1, user=user, title="test title", 
        description="description", url="http://www.google.com", is_active=True
    )


class ItemsTests(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(username='u1', email='user_1@gmail.com', password='p')
        self.user_2 = User.objects.create_user(username='u2', email='user_2@gmail.com', password='p')


    def test_urls_redirect_anon_users(self):
        """Items URLs should 302 redirect anonymous users to login page."""

        response = self.client.get('/items/')
        self.assertRedirects(response, '/login/?next=/items/', 302)
        
        response = self.client.get('/items/1/')
        self.assertRedirects(response, '/login/?next=/items/1/', 302)
        
        response = self.client.get('/items/create/')
        self.assertRedirects(response, '/login/?next=/items/create/', 302)
        
        response = self.client.get('/items/1/update/')
        self.assertRedirects(response, '/login/?next=/items/1/update/', 302)
        
        response = self.client.get('/items/1/delete/')
        self.assertRedirects(response, '/login/?next=/items/1/delete/', 302)


    def test_login_logout_urls(self):
        """Logging in should work with valid creds only. Logout should work"""
        # bad login should fail
        response = self.client.post('/login/', {'username': 'invalid_user', 'password': 'bad'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "enter a correct username and password")

        # valid login should succeed and redirect
        response = self.client.post('/login/', {'username': 'u1', 'password': 'p'})
        self.assertRedirects(response, '/items/', 302)

        # logout should succeed... 
        response = self.client.post('/logout/')
        self.assertRedirects(response, '/', 302)

        # and should redirect again once logged out
        response = self.client.get('/items/')
        self.assertRedirects(response, '/login/?next=/items/', 302)


    def test_read_items_with_no_items(self):
        """Read items page should work when there aren't any"""
        self.client.login(username='u1', password='p')
        # items list should be available to a logged in user
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Items")
        # but there shouldn't be any actual items yet
        self.assertQuerysetEqual(response.context['items'], [])


    def test_read_items_with_some_items(self):
        """Read items page should work when there are some"""
        self.client.login(username='u1', password='p')
        i = create_item(user=self.user_1, id=1)
        i.save()
        self.assertEqual(i.pk, 1)  # if i has a pk, save was successful

        # item 1 should be accessible to the user who created it
        response = self.client.get('/items/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test title")


    def test_cant_read_another_users_items(self):
        """Items should not be readable by other users"""
        # item 1 should NOT be accessible to another user
        self.client.login(username='u2', password='p')
        i = create_item(user=self.user_1, id=1)
        i.save()
        response = self.client.get('/items/1/')
        self.assertEqual(response.status_code, 404)


    def test_cant_read_inactive_items(self):
        """Items which have been deactivated should not be readable"""
        # after being set inactive, item 1 should NOT be accessible by user 1 anymore
        self.client.login(username='u1', password='p')
        i = create_item(user=self.user_1, id=1)
        i.is_active=False
        i.save()
        response = self.client.get('/items/1/')
        self.assertEqual(response.status_code, 404)


    def test_create_item(self):
        """User can create an item"""
        # user should be able to create an item
        self.client.login(username='u1', password='p')
        response = self.client.post('/items/create/', 
            {'title': 'test title', 
             'description': 'test description',
             'url': 'http://www.url.net'})
        self.assertRedirects(response, '/items/', 302)

        # Now read the new item
        response = self.client.get('/items/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test description")


    def test_update_item(self):
        """User can update one of his items"""
        self.client.login(username='u1', password='p')
        i = create_item(user=self.user_1, id=1)
        i.save()

        # update the item...
        response = self.client.post('/items/1/update/', 
            {'title': 'test title', 
             'description': 'updated description',
             'url': 'http://www.url.net'})
        self.assertRedirects(response, '/items/', 302)

        # ... and verify the update 
        response = self.client.get('/items/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "updated description")


    def test_delete_item(self):
        """User can delete one of his items"""
        self.client.login(username='u1', password='p')
        i = create_item(user=self.user_1, id=1)
        i.save()

        response = self.client.get('/items/1/delete/')
        self.assertContains(response, 'Confirm Delete?')

        post_response = self.client.post('/items/1/delete/')
        self.assertRedirects(post_response, '/items/', 302)

        # item should no longer be accessible...
        response = self.client.get('/items/1/')
        self.assertEqual(response.status_code, 404)

        # ...but should still be in the database with is_active=False
        i = Item.objects.get(pk=1)
        self.assertEqual(i.is_active, False)


    def test_cant_update_another_users_item(self):
        """User cannot update an item created by another user"""
        # user 2 creates an item
        i = create_item(user=self.user_2, id=1)
        i.save()
        # user 1 logs in
        self.client.login(username='u1', password='p')

        # update item fails (404)
        response = self.client.post('/items/1/update/', 
            {'title': 'test title', 
             'description': 'updated description',
             'url': 'http://www.url.net'})
        self.assertEqual(response.status_code, 404)


    def test_cant_delete_another_users_item(self):
        """User cannot delete an item created by another user"""
        # user 2 creates an item
        i = create_item(user=self.user_2, id=1)
        i.save()
        # user 1 logs in
        self.client.login(username='u1', password='p')

        # delete item fails (404)
        response = self.client.get('/items/1/delete/')
        self.assertEqual(response.status_code, 404)
