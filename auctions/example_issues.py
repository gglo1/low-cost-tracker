from dataclasses import field
from msilib import MSIMODIFY_DELETE
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404

#-------------------------------------------------------------------

class Listings(models.Model):
    ...

    ELECTRONICS = 'TCH'
    CLOTHING = 'CLT'
    UNKNOWN = 'UNK'
    FOOD = 'FOD'
    ART = 'ART'
    ACCESSORIES = 'AC'


    CATEGORY_CHOICES = [
    (ELECTRONICS, 'Electronics'),
    (FOOD, 'Food'),
    (ART, 'Art'),
    (CLOTHING, 'Clothing'),
    (ACCESSORIES, 'Accessories'),
    (UNKNOWN, 'Unknown'),
    ]

    category = models.CharField(max_length = 3, choices = CATEGORY_CHOICES, default = 'ELECTRONICS')


#         category = Listings.objects.filter(category = selection)


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/categories', blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Listings(models.Model):
    ...
    category = models.ForeignKey(..)
       
    c = Category.objects.get(category_id)
    listings = c.objects.all()
#-------------------------------------------------------------------

# def category_listing(request, selection):
#     try:
#         category = Listings.objects.filter(category = selection)
#     except:
#         category = None
#     return render(request, "auctions/category_listing.html", {
#           "category": category, 
#           "selection": selection, 
#           "categories": Listings.CATEGORY_CHOICES})

#  {% for item in category %}

def category_listing(request, category_id):
    listings = Listings.objects.filter(category = category_id)
    return render(request, "auctions/category_listing.html", {
            "listings": listings})

#  {% for listing in listings %}

#-------------------------------------------------------------------

@login_required(login_url='login')
def create_listing(request):
    ...

def login_view(request):
    if request.method == "POST":

        #...
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('index')

#-------------------------------------------------------------------

def view_listing(request, item):
    pass

def view_listing(request, listing_id):
    pass


#-------------------------------------------------------------------

        listing = get_object_or_404(pk = listing_id)
        # try:
        #     f = Listings.objects.get(pk = item)
        # except Listings.DoesNotExist:
        #     raise Http404("Listing not found")


#-------------------------------------------------------------------
   watchers = models.ManyToManyField(User, blank=True, related_name="watched_listings")

@login_required(login_url='login')
def my_watchlist(request):
    return render(request, "auctions/index.html", {
        'listings': request.user.watched_listings.order_by('-created_at'),
        'banner': 'My Watchlist'
    })

class Listing(models.Model):

    def watcher_count(self):
        return len(self.watchers.all())

    def toggle_watcher(self, user):
        user_is_watching = self.watchers.filter(id=user.id).exists()
        if user_is_watching:
            self.watchers.remove(user)
        else:
            self.watchers.add(user)

#-------------------------------------------------------------------

# fat model

class Listing():

    #...

    def minimum_bid(self):
        return max(self.starting_bid, 1+self.high_bid_amount())

    def high_bid(self):
        return self.bids.all().order_by('-created_at').first()

    def high_bid_amount(self):
        bid = self.high_bid()
        if bid:
            return bid.amount
        else:
            return 0 

#-------------------------------------------------------------------

def categories_view(request, chosen_category):
    if chosen_category == 'All':
        categories = []
        listings = Listing.objects.all()
        for listing in listings:
            if listing.category not in categories:
                categories.append(listing.category)
        if len(categories) == 0: categories = False
        return render(request, 'auctions/categories.html', {"categories":categories,
                                                            "All": True})
    else:
        listings = Listing.objects.filter(category=chosen_category)
        return render(request, 'auctions/categories.html', {"listings":listings,
                                                            "All": False,
                                                            "category": chosen_category})



{% extends "auctions/layout.html" %}


    {% block main %}
    {% if All %}
    <h2>Categories</h2>

    <article>
        {% if categories %}
        {% for category in categories %}
            <section>{{ category }} <a class="w3-button view-listing"  href="{% url 'categories' category %}">View {{ category }}</a></section>
        {% endfor %}
        {% else %}
            There are currenlty no active listings to show
        {% endif %}
    </article>
   
{% else %}
     <h2>{{category}}</h2>

    <article>
        {% if listings %}
        {% for listing in listings %}
            <section>{{ listing }} <a class="w3-button view-listing"  href="{% url 'listing' listing.id %}">View {{ listing.title }}</a></section>
        {% endfor %}
        {% else %}
            There are currenlty no active listings to show
        {% endif %}
    </article>
    {% endif %}
    {% endblock %}



class NewListing(forms.Form):    
    categories = [
        ('Other', 'Other'),
        ('Furniture', 'Furniture'),
        ('Outdoor', 'Outdoor'),
        ('Sports', 'Sports'),
        ('Automobile', 'Automobile'),
        ('Bicycles', 'Bicycle'),
        ('Apparel', 'Apparel'),
        ('Electronics', 'Electronics'),
    ]
 
    title = forms.CharField(label="Title:")    
    price = forms.IntegerField(label="Price:", min_value=0)    
    description = forms.CharField(label="Entry:", widget=forms.Textarea())
    image = forms.ImageField(label="Image:", required=False)   
    category = forms.CharField(label="Category", widget=forms.Select(choices=categories))


    urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:id>/close_listing", views.close_listing, name="close_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:id>", views.save_to_watchlist, name="save_to_watchlist"),
    path("remove_from_watchlist/<int:id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:id>", views.filter_category, name="filter_category"),
    path("<int:id>", views.listing, name="listing"),
    path("<int:id>/", views.comment_to_listing, name="comment_to_listing"),
    path("place_bid", views.place_bid, name="place_bid"),


------

User vs 


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, default = "", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} added {self.listing} to watchlist.'


Diff watchlinst
class Listing(models.Model):
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_listings")



-----

<article class="article">
    {% for l in listings %}
    
    {% if l.sold == False %}
    <div class="listingsgrid">

        {% for m in message %}
      <h2>{{m}}</h2>
      {% endfor %}

-----
def place_bid(request):
    if request.user.is_authenticated:
        # if request.method == "POST":
        #     msg =""
        #     form = BidsForm(request.POST)
        #     new_bid = int(form.data["new_bid"])
        #     id = form.data["id"]
        #     l = Listings.objects.get(pk=id)
        if request.method == "POST":
            msg =""
            form = BidsForm(request.POST)
            if form.is_valid():
                new_bid = form.cleaned_data["new_bid"]

----

    <form action="{% url 'place_bid' %}" method="POST">
        {% csrf_token %}
        <input type="hidden" name="id" value="{{listings.id}}">

--

Related field

class Listing(models.Model):

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="buyer")
    listing_category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="l_category")

    img = models.ImageField(upload_to='images/', blank=True)
    url_img = models.URLField()

-----

{% if user == listings.lister %}
    <a href="{% url 'close_listing' listings.id %}"><button>Close Listing</button></a>
{% endif %}


{% if user == listings.lister %}
    <a href="{% url 'close_listing' listings.id %}"><button>Close Listing</button></a>
{% endif %}

    {% if user == listings.lister %}
        <form action=""{% url 'close_listing' listings.id %}" method="POST">
            <button>Close Listing</button><
        </form>
    {% endif %}

    {% if user == listings.lister %}
        <form action=""{% url 'close_listing' listings.id %}" method="POST">
            <input type="submit">Close Listing</input>
        </form>
    {% endif %}

    #---------------

        created_at = models.DateTimeField(auto_now=True)

       comments = Comment.objects.filter(listing=entry).order_by('-created_at')


Probably better to display the items in the watchlist from newest to oldest. Easy way to do that is to add a field to the model: 
   created_at = models.DateTimeField(auto_now=True)
And then. Oops. Nevermind. Your watchlist is not an object. How about adding this to comments (i think you started to do so with creation_date), and then, when you display the comments, rather than
        comments = Comment.objects.filter(listing=entry)
you’d have
       comments = Comment.objects.filter(listing=entry).order_by(‘-created_at’)



