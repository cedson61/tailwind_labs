from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from braces.views import LoginRequiredMixin
from .models import Item


class ItemListView(LoginRequiredMixin, ListView):
    """return active items"""
    queryset = Item.active.all() # used instead of "model=" to filter inactives
    context_object_name = 'items'
    paginate_by = 5


class ItemDetailView(LoginRequiredMixin, DetailView):
    """return an item if it is active"""
    queryset = Item.active.all() # used instead of "model="" to filter inactives
    context_object_name = 'item'


class ItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    success_url = reverse_lazy('items:items_list')
    success_message = "New item created."


class ItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    success_url = reverse_lazy('items:items_list')
    success_message = "Item updated."


class ItemDeleteView(LoginRequiredMixin, DeleteView):
# In DeleteView we must add the success message manually, because
# SuccessMessageMixin hooks to form_valid which is not present in DeleteView.
    model = Item
    success_url = reverse_lazy('items:items_list')
    success_message = "Item deleted."

    # override delete method to merely *inactivate* the item, rather than 
    # deleting truly it from the database.
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())
