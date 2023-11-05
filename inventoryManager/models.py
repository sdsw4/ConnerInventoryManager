from django.db import models
from django.urls import reverse

# Create your models here.

# Highest level, the organization
# An organization will have multiple orders
class Organization(models.Model):
    name = models.CharField(max_length = 200)
    contact_name = models.CharField(max_length = 200)
    contact_email = models.CharField(max_length = 200)
    about = models.CharField(max_length = 200, blank = True)

    # Define the default string to return the name that represents the Model object.
    def __str__(self):
        return self.name

    # Returns the URL to access a particular instance of MyModelName.
    # Defining the method causes Django to automagically add a
    # "View on Site" button to the model's record editing screen
    # In the Admin site.
    def get_absolute_url(self):
        return reverse('organization-detail', args=[str(self.id)])

    def getNumOrders(self):
        return Order.objects.filter(organization = self).count()

# An order object
# An order is assigned to only one organization
# but an order can have many line-items
class Order(models.Model):
    posted = models.DateField()
    ordered = models.DateField(blank = True, null=True)
    completed = models.DateField(blank = True, null=True)

    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default = None)

    # Define the default string to return the name that represents the Model object.
    def __str__(self):
        return self.title

    # Returns the URL to access a particular instance of MyModelName.
    # Defining the method causes Django to automagically add a
    # "View on Site" button to the model's record editing screen
    # In the Admin site.
    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])