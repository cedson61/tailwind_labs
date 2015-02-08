from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from braces.views import LoginRequiredMixin
from .models import Item


class ItemListView(LoginRequiredMixin, ListView):
    """List of active items belonging to the current user"""
    model = Item
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        base_qs = super(ItemListView, self).get_queryset()
        return base_qs.filter(user=self.request.user)


class ItemDetailView(LoginRequiredMixin, DetailView):
    """Item detail if it is active and belongs to the current user"""
    model = Item
    fields = ['title', 'description', 'url']
    context_object_name = 'item'

    def get_queryset(self):
        base_qs = super(ItemDetailView, self).get_queryset()
        return base_qs.filter(user=self.request.user)


class ItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    fields = ['title', 'description', 'url']
    success_url = reverse_lazy('items:items_list')
    success_message = "New item created."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemCreateView, self).form_valid(form)


class ItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update an item if it is active and belongs to the current user"""
    model = Item
    fields = ['title', 'description', 'url']
    success_url = reverse_lazy('items:items_list')
    success_message = "Item updated."

    def get_queryset(self):
        base_qs = super(ItemUpdateView, self).get_queryset()
        return base_qs.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemUpdateView, self).form_valid(form)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an item if it is active and belongs to the current user"""
# In DeleteView we must add the success message manually, because
# SuccessMessageMixin hooks to form_valid which is not present in DeleteView.
    model = Item
    success_url = reverse_lazy('items:items_list')
    success_message = "Item deleted."

    def get_queryset(self):
        base_qs = super(ItemDeleteView, self).get_queryset()
        return base_qs.filter(user=self.request.user)

    # override delete method to merely *inactivate* the item, rather than 
    # deleting truly it from the database.
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())
