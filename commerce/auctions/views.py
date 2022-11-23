from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Active_list, Categorys, Watchlist

def massage(massage):
    return HttpResponse(f"<h1>{massage}</h1>")
    
def index(request):
    actives_list = Active_list.objects.all()
    categorys = Categorys.objects.all()
    return render(request, "auctions/index.html",{
        "categorys": categorys,
        "actives_list":actives_list
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def add_active(request):
    categorys = Categorys.objects.all()
    if request.method == "POST":
        title = request.POST["active_title"]
        price = request.POST["base_price"]
        image = request.POST["image"]
        description = request.POST["description"]
        
        categoryid = request.POST["category"]
        category = Categorys.objects.get(id = categoryid)
         

        userid = request.POST["userid"]
        user = User.objects.get(id = userid)
        
        
        add = Active_list(title=title, base_price=int(price), image=image, description=description, add_user=user, porpose_price=int(price), category=category)
        add.save()

        return HttpResponseRedirect(reverse(index))
    else:
        return render(request, "auctions/add_active.html",{
            "categorys": Categorys.objects.all(),
            "categorys": categorys
        })
    
def active(request, active_id):
    #take categorys name for dropdown
    categorys = Categorys.objects.all()
    # take slelected active
    active = Active_list.objects.get(id = active_id)
        # check watchlist
    if request.user.is_authenticated:
        user = User.objects.get( username = request.user)
        check = check_watchlist(active, user)
        
    return render(request, "auctions/active.html",{
        "active":active,
        "categorys": categorys,
        "check": check
    })

@login_required
def add_category(request):
    new = request.POST["new_category"]
    add = Categorys(name=new)
    add.save()
    return HttpResponseRedirect(reverse(add_active))


# take category id and return related active in category.html
def category(request, category_id):
    #take categorys name for dropdown
    categorys = Categorys.objects.all()
    # take related active
    category = Categorys.objects.get(id = category_id)
    category_list = category.category.all()
    return render(request, "auctions/category.html",{
        "actives":category_list,
        "categorys":categorys,
        "category":category
    })
    
    
# take porpose and update price
@login_required
def porpose(request, active_id):
    if (request.method == 'POST'):
        porpose = request.POST["porpose"]
        exporpose = Active_list.objects.get(id = active_id)
        if exporpose.porpose_price < int(porpose):
            exporpose.porpose_price = porpose
            exporpose.save()  
        else: 
            return massage("invalid porpose")
        
    return HttpResponseRedirect(reverse("active", args=(active_id)))

@login_required
def watchlist(request, user_id):
    #take categorys name for dropdown
    categorys = Categorys.objects.all()
    
    watchlist = Watchlist.objects.filter(user = user_id)

    return render(request, "auctions/watchlist.html", {
        "actives" : watchlist ,
        "categorys": categorys
    })
    
@login_required
def add_watchlist(request):
    #take categorys name for dropdown
    categorys = Categorys.objects.all()
    
    active_id = id = request.POST["active_id"]
    active = Active_list.objects.get(id = active_id)
    user_id = request.user
    # remove or add watchlist
    check = check_watchlist(active , user_id)
    watchlist = Watchlist(actives=active, user=user_id)
    if  not check :
        watchlist.save()
    else:
        watchlist = Watchlist.objects.get(actives=active, user=user_id)
        watchlist.delete()
        
    return HttpResponseRedirect(reverse("active", args=(active_id)))
    

def check_watchlist(active , user):
    is_it = False
    if Watchlist.objects.filter(user=user, actives=active):
        is_it = True
    
    return is_it
    