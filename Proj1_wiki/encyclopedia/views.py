import random
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, response
from django import forms
from markdown2 import Markdown

from . import util

class Search(forms.Form):
    search_field = forms.CharField(label="", widget=forms.TextInput(attrs={
      "placeholder": "Search Encyclopedia"
    }))

class Create(forms.Form):
    create_title = forms.CharField(label="Title of Page", widget=forms.TextInput(attrs={
        "placeholder": "Title"
    }))
    create_text = forms.CharField(label="Markdown of Content", widget=forms.Textarea)

class Edit(forms.Form):
    edit_text = forms.CharField(label="Edit Content", widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : Search()
    })

def entry(request, title):
    
    the_entry = util.get_entry(title)
    if (the_entry):
        entry_html = Markdown().convert(the_entry)
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "entry" : entry_html,
            "form" : Search()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title" : title,
            "form" : Search()
        })

def search(request):

    if request.method == "POST":
        search_form = Search(request.POST)
    
        if search_form.is_valid():
            entry_title = search_form.cleaned_data["search_field"]
            the_entry = util.get_entry(entry_title)
            if the_entry:
                return HttpResponseRedirect(reverse("entry", args=[entry_title]))
            else:
                related_entries = util.get_related_entries(entry_title)
                return render(request, "encyclopedia/search.html", {
                    "related_entries" : related_entries,
                    "title": entry_title,
                    "form": Search()
                })

def create(request):
    if request.method == "GET":
        print(request)
        return render(request, "encyclopedia/create.html", {
            "create_form": Create(),
            "form": Search()
        })

    elif request.method == "POST":
        create_form = Create(request.POST)

        if create_form.is_valid():
            form_title = create_form.cleaned_data["create_title"]
            form_text = create_form.cleaned_data["create_text"]
        else:
            error = "Form is invalid - Please fill the form again."
            return render(request, 'encyclopedia/create.html', {
                "create_form": Create(),
                "form": Search(),
                "error_msg": error
            })

        existing_entry = util.get_entry(form_title)
        if existing_entry:
            error = "This page already exists!"
            return render(request, "encyclopedia/create.html", {
                "create_form": Create(),
                "form": Search(),
                "error_msg": error
            })
        else:
            util.save_entry(form_title, form_text)
            return HttpResponseRedirect(reverse('entry', args=[form_title]))

def random_entry(request):
    rand_title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('entry', args=[rand_title]))

def edit(request, title):
    if request.method == "GET":
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": Search(),
            "edit_form": Edit(initial={'edit_text':entry}),
        })

    elif request.method == "POST":
        edit_form = Edit(request.POST)
        if edit_form.is_valid():
            text = edit_form.cleaned_data["edit_text"]
            util.save_entry(title, text)
            entry = util.get_entry(title)
            entry_md = Markdown().convert(entry)
            return render(request, "encyclopedia/entry.html", {
                "title" : title,
                "entry" : entry_md,
                "form" : Search()
            })
        else:
            error = "Form is invalid - Please fill the form again."
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "error_msg": error,
                "edit_form": edit_form,
                "form": Search()
            })

