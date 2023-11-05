from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from inventoryManager.models import *
from django.http import HttpResponse
from inventoryManager.forms import *

def OrganizationListView(request):
    organization_list = Organization.objects.all()

    context = {'organization_list' : organization_list}
    return render( request, 'inventoryManager/organization_list.html', context)

# Create your views here.
def index(request):
    organizations = Organization.objects.all()
    return render( request, 'inventoryManager/index.html', {'organizations':organizations})

# Method to view organizationDetails
def OrganizationDetailView(request, id):
    organization_id = id
    organization = Organization.objects.get(pk=organization_id)
    context = {'organization' : organization}
    orders = Order.objects.filter(organization = organization)
    context['order_list'] = orders

    return render( request, 'inventoryManager/organization_detail.html', context)

# New method to view organizationDetials
# This one is capable of displaying the create order form
# and edit order form as well as edit organization form
def OrganizationDetailViewEx(request, id):
    organization_id = id
    organization = Organization.objects.get(pk=organization_id)
    context = {'organization' : organization}
    orders = Order.objects.filter(organization = organization)
    context['order_list'] = orders

    if (request.method == 'POST'):
        if (request.POST['submit'] == "Edit Details"):
            organizationToUpdate = Organization.objects.get(pk=id)
            context['state'] = "Edit"
            # Populate the form with the organization's current data
            form = OrganizationForm(
            initial={"name" : organizationToUpdate.name,
                     "contact_name" : organizationToUpdate.contact_name,
                     "contact_email" : organizationToUpdate.contact_email,
                     "about" : organizationToUpdate.about
                    }
            )
            context['form'] = form

        elif (request.POST['submit'] == "Cancel" or request.POST['submit'] == "No") :
            return render( request, 'inventoryManager/organization_detail.html', context)

        elif (request.POST['submit'] == "Delete") :
            context['state'] = "Delete"
            
        elif (request.POST['submit'] == "Yes Delete"):
            organizationToDelete = Organization.objects.get(id=id)
            organization_data = {"organization_data" : organizationToDelete}
            if (organizationToDelete != None):
                organizationToDelete.delete()
                return redirect('organizations')

        elif request.POST['submit'] == "Submit":
            # Get form data and verify
            organizationToUpdate = Organization.objects.get(pk=id)
            context['state'] = "Edit"
            form = OrganizationForm(request.POST.copy())
            if form.is_valid():
               #clean the form data and assign it to something we can use
               data = form.cleaned_data
               
               #create new object from data
               organizationToUpdate.name = data['name']
               organizationToUpdate.contact_name = data['contact_name']
               organizationToUpdate.contact_email = data['contact_email']
               organizationToUpdate.about = data['about']

               #commit new object to database
               organizationToUpdate.save()

               # Redirect back to the organization's detail page
               return redirect('organization-detail', id)

    
    return render( request, 'inventoryManager/organization_detail.html', context)

# Method to create an organization
def CreateOrganization(request):
    form = OrganizationForm()

    if (request.method == 'POST'):
        if request.POST['submit'] == "Cancel":
            return redirect('organizations')
        elif request.POST['submit'] == "Submit":
            # Get form data and verify
            form = OrganizationForm(request.POST.copy())
            if form.is_valid():
               #clean the form data and assign it to something we can use
               data = form.cleaned_data
               
               #create new object from data
               newOrganization = Organization(
                   name = data['name'],
                   contact_name = data['contact_name'],
                   contact_email = data['contact_email'],
                   about = data['about']
                   )

               #commit new object to database
               newOrganization.save()

               # Redirect back to the organizations list page
               return redirect('organizations')

    context = {'form': form}
    context['state'] = "Create"
    return render(request, 'inventoryManager/organization_form.html', context)

# Method to edit an organization
def EditOrganization(request, id):
    organizationToUpdate = Organization.objects.get(pk=id)

    # Populate the form with the organization's current data
    form = OrganizationForm(
        initial={"name" : organizationToUpdate.name,
                 "contact_name" : organizationToUpdate.contact_name,
                 "contact_email" : organizationToUpdate.contact_email,
                 "about" : organizationToUpdate.about
                 }
        )

    if (request.method == 'POST'):
        if request.POST['submit'] == "Cancel":
            return redirect('organization-detail', id)
        elif request.POST['submit'] == "Submit":
            # Get form data and verify
            form = OrganizationForm(request.POST.copy())
            if form.is_valid():
               #clean the form data and assign it to something we can use
               data = form.cleaned_data
               
               #create new object from data
               organizationToUpdate.name = data['name']
               organizationToUpdate.contact_name = data['contact_name']
               organizationToUpdate.contact_email = data['contact_email']
               organizationToUpdate.about = data['about']

               #commit new object to database
               organizationToUpdate.save()

               # Redirect back to the organizations list page
               return redirect('organizations')

    context = {'form': form}
    context['state'] = "Edit"
    return render(request, 'inventoryManager/organization_form.html', context)

# Method to delete a project
def DeleteOrganization(request, id):
    # Get the data for the project to delete
    organizationToDelete = Organization.objects.get(id=id)
    organization_data = {"organization_data" : organizationToDelete}

    if (request.method == 'POST' and organizationToDelete != None):
        if request.POST['submit'] == "Cancel":
            # User changed mind, redirect back to the project detail page
            return redirect('organization-detail', id)
        elif request.POST['submit'] == "Delete":
            organizationToDelete.delete()
            return redirect('organizations')

    return render(request, 'inventoryManager/organization_delete.html', organization_data)

# Method to create an order
def OrganizationCreateOrder(request, id):
    organization_id = id
    form = OrderForm()
    organization = Organization.objects.get(pk=organization_id)

    if (request.method == 'POST'):
        if request.POST['submit'] == "Cancel":
            return redirect('organization-detail', organization_id)
        elif request.POST['submit'] == "Submit":
            # Get form data and verify
            order_data = request.POST.copy()
            order_data['organization_id'] = organization_id
        
            form = OrderForm(order_data)
            if form.is_valid():
                #clean the form data and assign it to something we can use
                data = form.cleaned_data

                newOrder = Order(
                    posted = data['posted'],
                    ordered = data['ordered'],
                    completed = data['completed'],
                    title = data['title'],
                    description = data['description'],
                    organization = organization,
                    )

                #commit the order to database
                newOrder.save()

                # Redirect back to the portfolio detail page
                return redirect('organization-detail', organization_id)

    context = {'form': form}
    context['organization'] = organization
    context['state'] = "Create"
    return render(request, 'inventoryManager/order_form.html', context)

def OrderDetailView(request, organizationId, orderId):
    return render(request, 'inventoryManager/order_detail.html')