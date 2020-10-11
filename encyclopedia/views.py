from django.shortcuts import render
from django import forms 
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
import random


class NewEntry(forms.Form):
    new_entry = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    new_description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control'}))

class EditEntry(forms.Form):
    edit_entry = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    edit_description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control'}))


def index(request):
    if request.method == "POST":
        title = request.POST.get('q')
        if title.lower() not in [entry.lower() for entry in util.list_entries()]:
            results = []
            for entry in util.list_entries():
                substring = title.lower()
                item = entry.lower()
                if item.find(substring) >= 0:
                    results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "title": title,
                "results": results
            })
        else:
            return render(request, "encyclopedia/view_entry.html", {
                "entry": util.get_entry(title),
                "title": title.capitalize()
            }) 
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def view_entry(request, title):
    if title.lower() not in [entry.lower() for entry in util.list_entries()]:
        return render(request, "encyclopedia/error.html", {
            "title": title.capitalize(),
            "error": 0
        })
    else:
        return render(request, "encyclopedia/view_entry.html", {
            "entry": util.get_entry(title),
            "title": title.capitalize()
        }) 


def add_entry(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            new_entry = form.cleaned_data["new_entry"]
            new_description = form.cleaned_data["new_description"]
            if new_entry.lower() in [entry.lower() for entry in util.list_entries()]:
                return render(request, "encyclopedia/error.html", {
                    "title": new_entry.capitalize(),
                    "error": 1
                })
            else:
                util.save_entry(new_entry, new_description)
                return HttpResponseRedirect(reverse("view_entry", args=(new_entry,)))
        else:
            return render(request, "encyclopedia/add_entry.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add_entry.html", {
            "form": NewEntry()
        })


def edit_entry(request, title):
    if request.method == "POST":
        form = EditEntry(request.POST)
        if form.is_valid():
            edit_description = form.cleaned_data["edit_description"]
            util.save_entry(title, edit_description)
            return render(request, "encyclopedia/view_entry.html", {
                "title": title,
                "entry": util.get_entry(title)
            })
        else:
            return render(request, "encyclopedia/edit_entry.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/edit_entry.html", {
            "form": EditEntry(initial={
                'edit_entry': title, 
                'edit_description': util.get_entry(title)
            }),
        })


def random_entry(request):
    title = random.choice(util.list_entries())
    return render(request, "encyclopedia/view_entry.html", {
        "title": title,
        "entry": util.get_entry(title)
    })
    