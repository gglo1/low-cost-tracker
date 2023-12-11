import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy

from .models import User, Listing, Category
from .forms import ListingForm, BidForm, CommentForm

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next", "index")
            return redirect(next_url)
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        next_url = request.GET.get("next", "index")
        return render(request, "auctions/login.html", {"next": next_url })


def logout_view(request):
    logout(request)
    return redirect("index")


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
        return redirect("index")
    else:
        return render(request, "auctions/register.html")


def index(request):
    return render(request, "auctions/index.html", context={
        'listings': Listing.objects.all().filter(active=True).order_by('-created_at'),
        'banner': 'All Existing Items',
    })

def search_listings(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        results = Listing.objects.filter(title__icontains=query, active=True)
        return render(request, 'auctions/search_results.html', {'listings': results, 'q': query})
    else:
        return HttpResponseBadRequest("Invalid Request Method")

from django.views.generic import ListView, CreateView, DeleteView, UpdateView
#------------------- Class-based View
class ListingsView(ListView): #current existing items function
    model = Listing
    template_name = 'auctions/index.html'
    context_object_name = "listings"

    def get_context_data(self):
        c = super().get_context_data()
        c['banner'] = 'All Existing Items'
        return c

    def get_queryset(self):
        return Listing.objects.filter(active=True).order_by('-created_at')


def listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        clicked = request.POST["doit"]
        if clicked == "toggle-watcher":
            listing.toggle_watcher(request.user)
            return redirect('listing', listing_id=listing.id)
        elif clicked == "bid":
            return redirect('bid', listing_id=listing.id)
            return HttpResponse("make a price change")
        elif clicked == "close-auction":
            listing.active = False
            listing.save()
            return redirect('my-listings')
        elif clicked == "add-comment":
            return redirect('add-comment', listing_id=listing_id)
        else:
            return HttpResponseServerError(f'Unknown button clicked')
    else:
        being_watched = listing.watchers.filter(id=request.user.id).exists()
        return render(request, "auctions/listing.html", {
            'listing': listing,
            'being_watched': being_watched,
        })

@login_required(login_url='login')
def my_listings(request): #if an item doesn't exist
    # user.id needed because user is SimpleLazyObject, not reconstituted
    listings1 = Listing.objects.filter(creator=request.user.id).order_by('-created_at')
    listings2 = request.user.listings.all().order_by('-created_at')

    return render(request, "auctions/index.html", {
        'listings': request.user.listings.order_by('-created_at'),
        'banner': 'Items Added By Me'
    })

@login_required(login_url='login')
def my_watchlist(request):
    return render(request, "auctions/index.html", {
        'listings': request.user.watched_listings.order_by('-created_at'),
        'banner': 'My Saved Items'
    })


@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        if "cancel" in request.POST: 
            return redirect('index')
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            form.save_m2m()
            messages.success(request, f'Item added successfully!')
            return redirect("index")
        else:
            messages.error(request, 'Problem adding the item. Details below.')	
    else: 
        form = ListingForm(initial={'starting_bid': 1})
    return render(request, "auctions/new_listing.html", {'form':form})

#-------- Class-based view
class ListingCreateView(CreateView):
    model = Listing
    template_name = "auctions/new_listing.html"
    form_class = ListingForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

@login_required(login_url='login')
# possible todo: prevent user to bid on his own listing
def bid(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        form.set_minimum_bid(listing.minimum_bid())
        if form.is_valid():
            bid = form.save(commit=False)
            bid.bidder = request.user
            bid.listing = listing
            bid.save()
            return redirect('listing', listing_id=listing_id)
        else:
            messages.error(request, "Problem with the price")
    else:
        form = BidForm(initial={'amount':listing.minimum_bid})
    return render(request, "auctions/bid.html", {
            'form': form,
            'listing': listing,
        }) 

@login_required(login_url='login')
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == "POST":
        if "cancel" in request.POST: 
            return redirect('listing', listing_id=listing_id)
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commentor = request.user
            comment.listing = listing
            comment.save()
            return redirect('listing', listing_id=listing_id)
        else:
            messages.error(request, 'Problem creating the comment. Details below.')	
    else: 
        form = CommentForm()
    return render(request, "auctions/listing.html", {
        'form':form, 'listing':listing, 'show_CommentForm':'yes'})


from django.http import JsonResponse
import json
def api_status(request):
    active_count = Listing.objects.filter(active=True).count()
    my_count = Listing.objects.filter(creator=request.user).count() if request.user.is_authenticated else 'n/a'

    status =  {
        'my_count': my_count,
        'active_count': active_count
    }
    return JsonResponse(status)

def categories(request):
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all().order_by('name'),
    })

class CategoriesView(ListView):
    model = Category
    template_name = 'auctions/categories.html'
    context_object_name = 'categories'

def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = Listing.objects.filter(categories = category, active=True)
    return render(request, "auctions/index.html", {
        'listings': listings,
        'banner': f'{category.name} Listings',
    })

class CategoryView(ListView):
    model = Listing
    template_name = 'auctions/category_listings.html'
    context_object_name = 'listings'

    def get_context_data(self):
        c = super().get_context_data()
        c['banner'] = 'Store Listings'
        category_id = self.kwargs["category_id"]
        category = Category.objects.get(id=category_id)
        c['category'] = category
        return c

    def get_queryset(self):
        return Listing.objects.filter(categories=self.kwargs['category_id'], active=True)


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'image']
    success_url = reverse_lazy('categories')

class CategoryEditView(UpdateView):
    model = Category
    fields = ['name', 'image']
    success_url = reverse_lazy('categories')

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')

from django.contrib.auth import views as auth_views
class PasswordChangedView(auth_views.PasswordChangeView):
    success_url = reverse_lazy('index')

@login_required(login_url='login')
def profile(request, username):
    # user = get_object_or_404(User, username=username)
    user = User.objects.get(username=username)
    return render(request, 'auctions/profile.html', {'user': user})

def contact(request):
    return render(request, 'auctions/contact.html')

from .forms import ProfileForm

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'auctions/edit_profile.html', {'form': form})

def home_view(request):
    return render(request, 'auctions/home.html')

def contact_us(request): #doesn't process in contact info
    if request.method == 'POST':
    #    return render(request, 'auctions/contact.html')
        return render(request, 'auctions/error.html')
    # return render(request, 'auctions/error.html')
    return render(request, 'auctions/contact.html')


