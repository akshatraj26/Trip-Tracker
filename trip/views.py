from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Trip, Note


class HomeView(TemplateView):
    template_name = "trip/index.html"
    
    
def trips_list(request):
    trips = Trip.objects.filter(owner=request.user)
    context = {
        'trips': trips
    }
    return render(request, 'trip/trip_list.html', context)


class TripCreateView(CreateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ['city', 'country', 'start_date', 'end_date']
    # template name model_form.html
    
    def form_valid(self, form):
        # owner_field = logged in User
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    
class TripUpdateView(UpdateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ['city', 'country', 'start_date', 'end_date']
    # uses the same templete as model_form.html
    

    
    
    
class TripDeteleView(DeleteView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    
    
    
class TripDetailView(DetailView):
    model = Trip
    # data stored on trip - also have note data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        trip = context['object']
        notes = trip.notes.all()
        context['notes'] = notes
        return context 
    

class NoteDetailView(DetailView):
    model = Note
    
    
def notes_list(request):
    notes = Note.objects.filter(trip__owner=request.user)
    context = {
        'notes': notes
    }
    return render(request, 'trip/note_list.html', context)



class NoteListView(ListView):
    model = Note
    
    def get_queryset(self):
        queryset = Note.objects.filter(trip__owner = self.request.user)
        return queryset



class NoteCreateView(CreateView):
    model = Note
    success_url = reverse_lazy('note-list')
    # fields = ['name', 'description', 'type', 'img', 'rating']
    fields = "__all__"
    
    def get_form(self):
        form = super(NoteCreateView, self).get_form()
        trips = Trip.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form
    
    
class NoteUpdateView(UpdateView):
    model = Note
    success_url = reverse_lazy('note-list')
    fields = '__all__'
    
    def get_form(self):
        form = super(NoteUpdateView, self).get_form()
        trips = Trip.objects.filter(owner = self.request.user)
        form.fields['trip'].queryset = trips
        return form
    

class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('note-list')
    
    # no template needed - send a post request to this url
    
    