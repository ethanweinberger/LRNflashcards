from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from flashcard_app.forms import UserForm, FlashcardForm, FlashcardGroupForm
from flashcard_app.models import Flashcard, FlashcardGroup
from random import randint

import json


# Create your views here.
def index(request):
    context = RequestContext(request)
    
    #Redirects the user to his home page if logged in
    if request.user.is_authenticated():
        print request.user
        return HttpResponseRedirect('/' + request.user.username + '/home/')
        
    #If not logged in, user will see the index page
    return render_to_response('flashcard_app/index.html', {}, context)


def home(request, username):
    context = RequestContext(request)
    
    current_user = request.user
    
    #Grabs all of the user's flashcard sets to display them
    flashcard_group_list = FlashcardGroup.objects.filter(user=current_user)
    
    return render_to_response('flashcard_app/home.html', {'flashcard_group_list': flashcard_group_list}, context)

def register_redirect(request):
    
    context = RequestContext(request)
    
    #This page is set to redirect the user to login after they register
    return render_to_response('flashcard_app/register_redirect.html', {}, context)

def register(request):
    context = RequestContext(request)
    registered = False
    
    user_form = UserForm(data=request.POST)
    if request.method == 'POST': #If the user has submitted the form, the request must be POST
        if user_form.is_valid(): #Checks to make sure the form has been completed properly

                new_user = user_form.save(commit = False) #Waits to save until password is hashed

                #Hashes the user's password to protect it
                new_user.set_password(new_user.password)
                new_user.save() #Saves to the database

                registered = True
                
                return HttpResponseRedirect('/register_redirect/')
        else:
            print user_form.errors #If the form was filled out improperly, the errors will be printed
    else:
        #If the request was not POST, then the user is looking for a blank form
        user_form = UserForm()
    
    return render_to_response(
            'flashcard_app/register.html',
            {'user_form': user_form, 'registered': registered},
            context)

def user_login(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username, password = password)
        
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            message = "Invalid username and/or password"
            return render_to_response('flashcard_app/login.html', {'message': message}, context)
    else:
        return render_to_response('flashcard_app/login.html', {}, context)
    
def user_logout(request):
    logout(request)
    
    return HttpResponseRedirect('/')
    
@login_required
def create_flashcard_group(request, username):
    context = RequestContext(request)
    
    created = False
    
    #If we're POSTing, that means the form has been submitted and
    #we can grab data from it
    if request.method == 'POST': 
        flashcard_group_form = FlashcardGroupForm(data=request.POST)
        
        if flashcard_group_form.is_valid():
            flashcard_group = flashcard_group_form.save(commit = False)
            
            current_user = request.user
            flashcard_group.user = current_user
            flashcard_group.save()
            
            created = True
            
            return HttpResponseRedirect("/" + request.user.username + "/home/")
        else:
            print flashcard_group_form.errors
    #If request is a GET, just render a blank form
    else: 
        flashcard_group_form = FlashcardGroupForm()
        
    return render_to_response('flashcard_app/create_flashcard_group.html', {'flashcard_group_form': flashcard_group_form}, context)
    
@login_required
def create_flashcard(request, username, groupname):
    context = RequestContext(request)
    
    failed = False

    if request.method == 'POST':
        flashcard_form = FlashcardForm(data=request.POST)
        
        if flashcard_form.is_valid():
            flashcard = flashcard_form.save(commit = False)
            
            current_user = request.user #Grabs the current user from Django

            flashcard.group = FlashcardGroup.objects.get(name=groupname, user = current_user)
            
            try:
                duplicate = Flashcard.objects.get(group = flashcard.group, frontside = flashcard.frontside, backside = flashcard.backside)
                failed = True
            except Flashcard.DoesNotExist:
                flashcard.save()

        else:
            print flashcard_form.errors
    else:
        current_user = request.user #Grabs the current user from Django
        flashcard_form = FlashcardForm()
        
    group = FlashcardGroup.objects.get(name=groupname, user = current_user)
    print group.front_side, group.back_side
    return render_to_response('flashcard_app/create_flashcard.html', {'flashcard_form': flashcard_form, 'groupname': groupname, 'failed': failed, 'group' : group}, context)

@login_required   
def view_flashcard_groups(request, username):
    context = RequestContext(request)
    
    current_user = request.user
    
    flashcard_group_list = FlashcardGroup.objects.filter(user=current_user) #Grabs the list of cards matching the current user
    
    return render_to_response('flashcard_app/view_flashcard_groups.html', {'flashcard_group_list':flashcard_group_list}, context)

@login_required
def view_flashcards(request, username, groupname):
    context = RequestContext(request)
    
    current_user = request.user
    
    current_group = FlashcardGroup.objects.get(name = groupname)
    
    flashcard_list = Flashcard.objects.filter(group = current_group) #Grabs the list of cards matching the current user and group
    
    return render_to_response('flashcard_app/view_flashcards.html', {'flashcard_list':flashcard_list, 'group': current_group}, context)

@login_required
def practice_flashcards(request, username, groupname, side):
    context = RequestContext(request)
    current_user = request.user
    
    current_group = FlashcardGroup.objects.get(name = groupname)
    
    flashcard_list = Flashcard.objects.filter(group = current_group)
    
    for item in flashcard_list:
        item.times_wrong = 0
        item.active = True
        item.save()
    
    #Grabs the list of cards matching the current user
    flashcard_list_length = Flashcard.objects.filter(group = current_group).count()
    
    if flashcard_list_length > 0:
        rand_card_index = randint(0,flashcard_list_length-1) #Picks a random number in the range of possible indexes
        my_card = flashcard_list[rand_card_index] #Saves the card in a variable
    
        return render_to_response('flashcard_app/practice_flashcards.html', {'my_card':my_card, 'groupname':groupname, 'side': side}, context)
    
    else:
        return HttpResponse("No cards in this group")
@login_required    
def check_flashcard(request):
    context = RequestContext(request)
    
    if request.is_ajax():
        if request.method == "POST":
            
            answer = request.POST['answer']
            question = request.POST['question']
            true_back = request.POST['true_back']
            side = request.POST['side']
            
            group = FlashcardGroup.objects.get(name=request.POST['groupname'])
            
            
            if side == 'front':
                try:
                    Flashcard.objects.get(frontside = question, backside = answer, group = group)
                    return HttpResponse("Correct")
                except:
                    try:
                        f = Flashcard.objects.get(frontside = question, backside = true_back, group = group)
                    except Exception, err:
                        print Exception, err

                    print "got here"
                    f.times_to_repeat += 2
                    f.times_wrong += 1
                    f.save()
            elif side == 'back':
                try:
                    #If the user is doing a drill where flashcard back's are the prompts and fronts
                    #are the answers, then the variables in the 'get' must be reversed
                    Flashcard.objects.get(frontside = answer, backside = question, group = group)
                    return HttpResponse("Correct")
                except:
                    try:
                        f = Flashcard.objects.get(frontside = true_back, backside = question, group = group)
                    except Exception, err:
                        print Exception, err

                    print "got here"
                    f.times_to_repeat += 2
                    f.times_wrong += 1
                    f.save()
            
        return HttpResponse('Wrong')
    
@login_required
def generate_flashcard(request, username, groupname, side):
    context = RequestContext(request)
    current_user = request.user
    
    current_group = FlashcardGroup.objects.get(name = groupname, user = current_user)

    flashcard_list = Flashcard.objects.filter(group = current_group)
    
    if side == 'front':
    
        try:
            used_card = Flashcard.objects.get(frontside = request.POST['question'], group = current_group)
        except Exception, err:
            print Exception, err
            
    elif side == 'back':
        
        #Since the user is testing the flashcards in reverse, the question/answer and frontside/backside
        #roles need to be reversed
        try:
            used_card = Flashcard.objects.get(backside = request.POST['question'], group = current_group)
        except Exception, err:
            print Exception, err

    result = request.POST['result']    

    if used_card.times_to_repeat == 0:  
        used_card.active = False
        used_card.save()
    else:
        used_card.times_to_repeat -= 1
        used_card.save()


    active_cards = Flashcard.objects.filter(group = current_group, active = True)

    flashcard_list_length = Flashcard.objects.filter(group=current_group, active = True).count()

    if Flashcard.objects.filter(active = True, group = current_group).count() > 0:
        print Flashcard.objects.filter(active = True, group = current_group)
        rand_card_index = randint(0,flashcard_list_length-1) #Picks a random number in the range of possible indexes
        
        my_card = active_cards[rand_card_index] #Saves the card in a variable
        print 'got here'
        return render_to_response('flashcard_app/flashcard.html', {'my_card':my_card, 'side': side}, context)
    
    
    else:
        inactive_cards = Flashcard.objects.filter(group = current_group, active = False)
        print "got here"
        for item in inactive_cards:
            item.active = True
            item.save()
        print "got here 2"
        return HttpResponse("Drill finished!")
    return HttpResponse("ERROR")

@login_required
def delete_flashcard_group(request):
    context = RequestContext(request)
    current_user = request.user

    groupname = request.POST['groupname']
    
    current_group = FlashcardGroup.objects.get(name = groupname, user = current_user)
    current_group_flashcards = Flashcard.objects.filter(group = current_group)
    
    current_group_flashcards.delete()
    current_group.delete()
    
    return HttpResponse("Success")

@login_required
def delete_flashcard(request):
    context = RequestContext(request)
    current_user = request.user

    groupname = request.POST['groupname']
    flashcardName = request.POST['flashcardName']
    frontside, backside = flashcardName.split(' / ')
    
    current_group = FlashcardGroup.objects.get(name = groupname, user = current_user)
    flashcard_to_delete = Flashcard.objects.get(group = current_group, frontside = frontside, backside = backside)
    
    flashcard_to_delete.delete()
    
    return HttpResponse("Success")

@login_required
def results(request, username, groupname, side):
    context = RequestContext(request)
    current_group = FlashcardGroup.objects.get(user = request.user, name = groupname)
    
    answered_incorrectly = Flashcard.objects.filter(group = current_group, times_wrong__gt=0)
    
    answered_correctly_count = Flashcard.objects.filter(group = current_group, times_wrong = 0).count()
    total_count = Flashcard.objects.all().count()

    
    score = float(answered_correctly_count)/total_count * 100
    
    return render_to_response('flashcard_app/results.html', {'answered_incorrectly': answered_incorrectly, 'groupname': groupname, 'score': score}, context)

    
    
    
        