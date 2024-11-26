# File created because of operations that were used in multiple
# function in views.py

from encyclopedia import serializers
from encyclopedia import models
from django.shortcuts import get_object_or_404

from . import util
import markdown2


# Função auxiliar para verificar se o usuário tem o role necessário
def check_role(request):
    user_id  = request.data.get('user_id')
    user_role = request.data.get('user_role')
    user = get_object_or_404(models.User, id=user_id)
    if user.role == user_role:
        return True
    else:
        return False


# This function gets all the entries, check if the input given by the user already
# exists in the wiki, and in case it does, retrive the content for that input and 
# sends it all back.
def checkInput(input):
    entries = util.list_entries()
    
    for entryvar in entries:
        if input.casefold() == entryvar.casefold():
            entryExists = True
            content = markdown2.markdown(util.get_entry(input))
            break
        else:
            entryExists = False
            content = "error"

    return(entryvar, content, entryExists)

# Simple function to check substring matching given a search input given by
# the user.
def checkSearch(input):
    searchMatches = []
    matches = False
    entries = util.list_entries()
    
    for entryvar in entries:
        if input.casefold() in entryvar.casefold():
            searchMatches.append(entryvar)
            matches = True
    
    return(searchMatches, matches)

    