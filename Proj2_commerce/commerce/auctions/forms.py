from django.db.models.fields import TextField
from django.forms import ModelForm, Textarea, NumberInput
from django.forms.widgets import Select, TextInput

from .models import *

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'photo', 'category', 'price']
        widgets = {
            'description': Textarea(attrs={'class': 'descp'}),
            'title': TextInput(attrs={'class': 'field'}),
            'photo': TextInput(attrs={'class': 'field'}),
            'category': Select(attrs={'class': 'field'}),
            'price': NumberInput(attrs={'class': 'numfield'}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'class': 'descp'})
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        widgets = {
            'price': NumberInput(attrs={'class': 'numfield'})
        }
