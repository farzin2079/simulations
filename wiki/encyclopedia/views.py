from django.urls import reverse
import random
from django.shortcuts import render,redirect
from django import forms

import markdown

from . import util

class ImportEnteries(forms.Form):
    new_title = forms.CharField(label='',widget=forms.TextInput(attrs={
        "placeholder": "title"}))
    new_content = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"}))
    
class Search(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search Qwikipedia"}))

class Edit(forms.Form):
    new_content = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "num_entry": len(util.list_entries()),
        "search_form": Search()
    })

def entry(request, title):
    # take markdown and tern to html
    return render(request , "encyclopedia/enteries.html",{
        "detals" : markdown.markdown(util.get_entry(title)),
        "title": title,
        "search_form": Search()
    })
    
def create(request):
    if request.method =='POST':
        form = ImportEnteries(request.POST)
        #check it is valid
        if form.is_valid():
            new_content = form.cleaned_data['new_content']
            new_title = form.cleaned_data['new_title']
            # if title exist make error
            list = util.list_entries()
            if new_title in list:
                return render(request, "encyclopedia/create.html", {
                "form": "titel is aready exist",
                "search_form": Search()
            })
                # if allright seve new entry
            util.save_entry(new_title, new_content)
            return redirect(reverse("entry", args=[new_title]))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form,
                "search_form": Search()
            })
    return render(request, "encyclopedia/create.html",{
        "form" : ImportEnteries(),
        "search_form": Search()
        })

def edit(request, title):
    if request.method =='POST':
        form = Edit(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data['new_content']
            list = util.list_entries()
            if title in list:
                util.save_entry(title, new_content)
                return redirect(reverse("entry", args=[title]))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "title": "not valid",
                "search_form": Search()
            })
    return render(request, "encyclopedia/edit.html",{
        "form" : Edit(),
        "title": title,
        "search_form": Search()
        })

def search(request):
    """ Loads requested title page if it exists, else displays search results """

    # If search page reached by submitting search form:
    if request.method == "POST":
        form = Search(request.POST)

        # If form is valid try to search for title:
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_md = util.get_entry(title)

            print('search request: ', title)

            if entry_md:
                # If entry exists, redirect to entry view
                return redirect(reverse('entry', args=[title]))
            else:
                # Otherwise display relevant search results
                related_titles = util.related_titles(title)

                return render(request, "encyclopedia/search.html", {
                "title": title,
                "related_titles": related_titles,
                "search_form": Search()
                })

    # Otherwise form not posted or form not valid, return to index page:
    return redirect(reverse('index'))

def random_title(request):
    """ Takes user to a random encyclopedia entry """

    # Get list of titles, pick one at random:
    titles = util.list_entries()
    title = random.choice(titles)

    # Redirect to selected page:
    return redirect(reverse('entry', args=[title]))

def delete(request, title):
    # delete entry and redirect index
    if util.delete_entry(title):
        return redirect(reverse('index'))
    
    