from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Secret, Like
from django.contrib.auth import logout

def index(request):
    return render(request, 'secret_keep/index.html')

def register(request):
    data={
    'f_name':request.POST['f_name'],
    'l_name':request.POST['l_name'],
    'email':request.POST['email'],
    'password':request.POST['password'],
    'conf_password':request.POST['conf_password']
    }
    # dictionary key calling the form data that is being inputted
    new_user=User.objects.register(data)
    print result
    # register in this line refers to register in the models line
    # This is running the model function, running it on this dictionary. This is the connecting factor between the views and the models.
    if new_user['errors']:
        for error in new_user['errors']:
            messages.add_message(request, messages.ERROR,error)
        return redirect('/')
        # the return MUST BE outside of the forloop in order for this to loop through all the errors befroe returning
    else:
# if what's in models (refferred to with result) is not placing anything in the errors list
            request.session['user']=new_user['user'].id
# modifying our session (user is user key), creates a new user id, refferring to user....
            return redirect('/secrets',data)
    return render(request, 'secret_keep/secrets.html', data)

def login(request):
    data={
    'email':request.POST['email'],
    'password':request.POST['password']
    }
    found_user=User.objects.login(data)
# Assign more descriptive terms for what this variable represents
    if found_user['errors']==None:
        request.session['user']=found_user['user'].id
        # request.session['User']=result['User'].email
        return redirect('/secrets',data)
    else:
        for error in found_user['errors']:
            messages.add_message(request, messages.ERROR,error)
        return redirect('/')
    return redirect('/secrets',data)

def logout_view(request):
    logout(request)
    return render(request, 'secret_keep/index.html')

def secrets(request):
    current_user=User.objects.get(id=request.session['user'])
    all_secrets= Secret.objects.all().order_by('-created_at')
    secrets_list=[]
    for my_secret in all_secrets:
        my_secret.liked=True
        my_secret.num_liked=Like.objects.filter(secret=my_secret).count()
# Automatically assuming that that this user has liked this secret

        try:
            Like.objects.get(user=current_user, secret=my_secret)
# associating both together
        except:
            my_secret.liked=False
        secrets_list.append(my_secret)
    # And if you don't find it, we're changing it to false
            # adding new property

    data={
    #Key in dictionary is variable name in template
        'user':User.objects.get(id=request.session['user']),
        'secrets': secrets_list
        # Key is variabel name
        }
    return render(request, 'secret_keep/secrets.html', data)

def post_secret(request):
    current_user=User.objects.get(id=request.session['user'])
    my_secret=Secret.objects.create(secret=request.POST['secret'], user=current_user)
# using objects as much as possible, if you assign variables, this makes it easier to understand too.

    return redirect('/secrets')

def add_like(request, my_secret_id):
# If we are dealing with the passing of a variable to connect two things together,
# we need to pass that thing into the def so it can be recognized
    a_secret=Secret.objects.get(id=my_secret_id)
    # The parameter we passed
    a_user=User.objects.get(id=request.session['user'])
    Like.objects.create(secret=a_secret, user=a_user)
    return redirect('/secrets')

def destroy(request,my_secret_id):
    my_secret=Secret.objects.get(id=my_secret_id).delete()
    return redirect('/secrets')
