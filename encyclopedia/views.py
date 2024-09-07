from django.shortcuts import render
from django.contrib import messages
import random
import os
from . import helpers
from . import util


def index(request):
    searchInput = request.GET.get("q")
    
    # Deals with the search input given by the user when searching the wiki 
    if searchInput:
        content = helpers.checkInput(searchInput)
        
        # Checking if the entry exists, where content[2] is a bool. This is false
        # when the search input doesn't match any of the wiki entries
        if not content[2]:
            # Function that will check for substrings in the name of the wiki
            # entries and compare to the input given by the user
            matches = helpers.checkSearch(searchInput)
            
            # Verifiy if there were any matches, and if there were, render the page with them
            if matches[1]:
                return render(request, "encyclopedia/index.html", {
                    "entries": matches[0],
                    "searchResult": "Search Result"
                })
                
        # If the input matches with an entry on the wiki, render the page       
        return render(request, "encyclopedia/entry.html", {
            "entryName": content[0],
            "entry": content[1],
            "entryExists": content[2],
        })
    else: 
        # If no search input given, render the index page with all the entries
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    
# When a link is clicked on the index page, it renders the link clicked
def entry(request, entry):
    content = helpers.checkInput(entry)
    return render(request, "encyclopedia/entry.html", {
        "entryName": content[0],
        "entry": content[1],
        "entryExists": content[2],
    })
    

def newPage(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('textArea')

        # Check if user gave a title and wrote some content to be added 
        if len(title) == 0 or len(content) == 0:
            messages.error(request, "Title and content required!")
            return render(request, "encyclopedia/editor.html")

        # Check if entry already exists 
        if helpers.checkInput(title)[2]:
            messages.error(request, "Entry already exists!")
            return render(request, "encyclopedia/editor.html")
        else:
            # If the entry doesn't already exists, add it, with the title getting
            # a # and a double line break
            content = "#" + title + "\n\n" + content
            title = title.replace(" ", "-")
            util.save_entry(title, content)
            
            content = helpers.checkInput(title)
            return render(request, "encyclopedia/entry.html", {
                "entryName": content[0],
                "entry": content[1],
                "entryExists": content[2],
            })
            
    else:
        return render(request, "encyclopedia/editor.html")
    
def edit(request, entry):
    if request.method == 'POST':
        
        if "delete" in request.POST:
            os.remove(f"entries/{entry}.md")
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
        
        # After being edited, we add the text back into the entry file
        # with its title at the top (titles cannot be edited)
        content = request.POST.get('textArea') 
        content = "#" + entry + "\n\n" + content
        content = bytes(content, "utf-8")
        
        util.save_entry(entry, content)
        content = helpers.checkInput(entry)
        return render(request, "encyclopedia/entry.html", {
            "entryName": content[0],
            "entry": content[1],
            "entryExists": content[2],
        })
    # This will render the editor page with the content of the entry
    # in the text area without the title
    else:
        content = util.get_entry(entry)
        
        return render(request, "encyclopedia/editor.html", {
            "entryName": entry,
            "entry": content.split("\n",2)[2],
        })
        
 
def randomPage(request):
    entries = util.list_entries()
    content = helpers.checkInput(random.choice(entries))
    print(content)
    return render(request, "encyclopedia/entry.html", {
        "entryName": content[0],
        "entry": content[1],
        "entryExists": content[2],
    })
