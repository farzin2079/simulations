from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Categorys, Comment, Bids
from .forms import ListingForms


def massage(massage):
    return HttpResponse(f'<h1>{massage}</h1><a href="/">home</a>')
    
def index(request):
    actives_list = Listing.objects.all()
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
    if request.method == "POST":
        title = request.POST['title']
        image = request.POST['image']
        category = request.POST['category']
        description = request.POST['description']
        base_price = request.POST['base_price']
        add_user = request.user
        
        active  = Listing(title=title , image=image, category=Categorys.objects.get(pk=category), description=description, base_price=base_price, add_user=add_user)
        active.save()
        # add bids
        bid = Bids(user=add_user, price=base_price, active=active)
        bid.save()
        
        return redirect('index')
    else:
        return render(request, "auctions/add_active.html",{
            "categorys": Categorys.objects.all(),
            "forms": ListingForms
        })
    
def active(request, active_id):
    #take categorys name for dropdown
    categorys = Categorys.objects.all()
    # take slelected active
    active = Listing.objects.get(id = active_id)
    # check watchlist
    check = False
    if request.user.is_authenticated:
        user = User.objects.get( username = request.user)
        # check = check_watchlist(active, user)
        
    comments = comment(active_id)
    bids = Bids.objects.get(active=active)
        
    return render(request, "auctions/active.html",{
        "active":active,
        "categorys": categorys,
        "check": check,
        "comments" :comments,
        "bids":bids
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
def bids(request, active_id):
    if (request.method == 'POST'):
        porpose = request.POST["porpose"]
        user = request.user
        active = Listing.objects.get(id = active_id)
        exbid = Bids.objects.get( active=active)
        if (exbid.price )<= int(porpose):
            newbid = Bids(user=user, price=porpose,active=active)
            exbid.delete()
            newbid.save() 
            active.bids = newbid
            active.save()
        else: 
            return massage("invalid porpose")
        
    return HttpResponseRedirect(reverse("active", args=(active_id)))

@login_required
def watchlist(request, user_id):
    #take categorys name for dropdown
    categorys = Categorys.objects.all()
    
    watchlist = User.objects.get(id = user_id)

    return render(request, "auctions/watchlist.html", {
        "actives" : watchlist ,
        "categorys": categorys
    })
    
@login_required
def add_watchlist(request):
    #take categorys name for dropdown
    categorys = Categorys.objects.all()
    
    active_id = request.POST["active_id"]
    active = Listing.objects.get(id = active_id)
    # remove or add watchlist
    check = check_watchlist(active , request.user)
    if  not check :
        User.watchlist.add(active)
    else:
        User.watchlist.delete(active)
        
    return HttpResponseRedirect(reverse("active", args=(active_id)))
    

def add_comment(request, active_id):
    comment = request.POST["comment"]
    user = request.user
    
    active = Listing.objects.get( pk= active_id)
    add_comment = Comment(user=user, comment=comment, active=active)
    add_comment.save()
    
    return HttpResponseRedirect(reverse("active", args=(active_id)))

def cancel(request):
    cancel = request.POST['cancel']
    
    active = Listing.objects.get( id = cancel)
    active.delete()
    
    return HttpResponseRedirect(reverse(index))

def close(request):
    close = request.POST['close']
    
    active = Listing.objects.get(id = close)
    winner = Bids.objects.get(active = active)
    active.delete()
    
    return massage(f"{winner.user} is winner with {winner.price} porpose")
    

def check_watchlist(active , user):
    is_it = False
    if active in User.objects.get(id=user.id).watchlist :
        is_it = True
        
    return is_it
    
def comment(active_id):
    comment = Comment.objects.filter( active = active_id)
    
    return comment