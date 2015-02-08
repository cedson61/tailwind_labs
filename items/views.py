from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from braces.views import LoginRequiredMixin
from .models import Item


class UserFilterMixin(object):
    """Used in CBVs below to ensure a user can only see /edit his own items."""
    def get_queryset(self):
        queryset = super(UserFilterMixin, self).get_queryset()
        return queryset.filter(user=self.request.user)


class ItemListView(LoginRequiredMixin, UserFilterMixin, ListView):
    """List of active items belonging to the current user"""
    model = Item
    context_object_name = 'items'
    paginate_by = 5


class ItemDetailView(LoginRequiredMixin, UserFilterMixin, DetailView):
    """Item detail if it is active and belongs to the current user"""
    model = Item
    fields = ['title', 'description', 'url']
    context_object_name = 'item'


class ItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    fields = ['title', 'description', 'url']
    success_url = reverse_lazy('items:items_list')
    success_message = "New item created."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemCreateView, self).form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserFilterMixin, SuccessMessageMixin, UpdateView):
    """Update an item if it is active and belongs to the current user"""
    model = Item
    fields = ['title', 'description', 'url']
    success_url = reverse_lazy('items:items_list')
    success_message = "Item updated."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemUpdateView, self).form_valid(form)


class ItemDeleteView(LoginRequiredMixin, UserFilterMixin, DeleteView):
    """Delete an item if it is active and belongs to the current user"""
# In DeleteView we must add the success message manually, because
# SuccessMessageMixin hooks to form_valid, which is not present in DeleteView.
    model = Item
    success_url = reverse_lazy('items:items_list')
    success_message = "Item deleted."

    # override delete method to merely "soft delete" the item.
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())
