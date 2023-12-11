from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.core.validators import MinValueValidator
from django.urls import reverse


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='images/profiles', blank=True, null=True)

    def active_listings(self):
        return Listing.objects.filter(active = True)
    
    def my_listings(self):
        return Listing.objects.filter(creator = self)


class Listing(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='images/listings', blank=True)
    active = models.BooleanField(default=True)
    # starting_bid = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2) 
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_listings")
    categories = models.ManyToManyField('Category', blank=True, related_name="listings")

    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse('listing', kwargs={'listing_id': self.pk})

    def watcher_count(self):
        return len(self.watchers.all())

    def toggle_watcher(self, user):
        user_is_watching = self.watchers.filter(id=user.id).exists()
        if user_is_watching:
            self.watchers.remove(user)
        else:
            self.watchers.add(user)

    def bid_count(self):
        return len(self.bids.all())

    def minimum_bid(self): #checks for lower price
        return max(self.starting_bid, self.high_bid_amount())

    def high_bid(self):
        return self.bids.all().order_by('-created_at').first()

    def high_bid_amount(self): #checks for lower price
        bid = self.high_bid()
        if bid:
            return bid.amount
        else:
            return 0
            
    def comment_count(self):
        return len(self.comments.all())


class Bid(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)  


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=500)


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/categories', blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    

