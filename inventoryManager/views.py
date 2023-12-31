from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from inventoryManager.models import *
from django.http import HttpResponse
from inventoryManager.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def userAuthCheck(user, expectedUser):
    if request.user.is_authenticated and organization.associatedUser == request.user:
        # User's logged in, so we get their object. we also check if this is their organization
        # and let them in
        return True
    elif request.user.is_authenticated and organization.associatedUser != request.user:
        # this isn't the user's organization. okay at this point whoever keeps fucking with stuff
        # needs to get a life. unless we hired that one to poke.
        return render(request, 'inventoryManager/denied.html')
    else:
        # user's anonymous, so we can't let them continue
        # let them know by bringing them to the login page.
        return redirect('login-user')

# Create your views here.
def index(request):
    organizations = Organization.objects.all()
    context = {'organizations':organizations}

    # user authenticated specific stuff
    if request.user.is_authenticated:
        # User's logged in, go get their username
        # also, we want the template to be slightly different, but that's on the template side
        context['currentuser'] = request.user
    else:
        # user's anonymous, so we don't have to do anything
        # some placeholder stuff is here in case we want to tinker with anonymous access later
        1+1

    return render( request, 'inventoryManager/index.html', context)

def denied(request):
    return render(request, 'inventoryManager/denied.html')

# ///////////////////////////////////////////////
# //         BEGIN USER SPECIFIC STUFF         /////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////

# Method to create a user
def CreateUser(request):
    form = UserCreateForm()

    if (request.method == 'POST'):
        if request.POST['submit'] == "Cancel":
            return redirect('index')
        elif request.POST['submit'] == "Submit":
            # Get form data and verify
            form = UserCreateForm(request.POST.copy())
            if form.is_valid():
               #clean the form data and assign it to something we can use
               data = form.cleaned_data
               
               #create new object from data
               newUser = User(
                   username = data['username'],
                   email = data['email'],
                   first_name = data['first_name'],
                   last_name = data['last_name'],
                   )
               #have to use a separate method to set a user's password
               # simply setting it as part of the create user object won't work
               #because the password has to be made a hash.
               # https://www.reddit.com/r/django/comments/xwy9uw/authenticate_method_of_djangocontribauth/
               newUser.set_password(data['password'])

               #commit new object to database
               newUser.save()

               # Redirect back to the organizations list page
               return redirect('index')

    context = {'form': form}
    context['state'] = "Create"
    return render(request, 'inventoryManager/create_user_form.html', context)

#View method for a user to login
def LoginUser(request):
    form = UserLoginForm()
    context = {'state' : "Login"}
    context['form'] =  form

    if (request.method == 'POST'):
        if request.POST['submit'] == "Cancel":
            return redirect('index')
        elif request.POST['submit'] == "Submit":
            # Get form data and verify
            form = UserLoginForm(request.POST.copy())
            if form.is_valid():
               #clean the form data and assign it to something we can use
               data = form.cleaned_data
               username = data['username']
               password = data['password']
               
               # get submitted details and try to authenticate
               user = authenticate(username=username, password=password)

               if user is not None:
                   # user entered good data
                   login(request, user)
                   return redirect('index')
               else:
                   #User entered some bad data
                   form = UserLoginForm(
                       initial={
                           "username" : data['username'],
                           }
                       )
                   context['form'] =  form
                   return render(request, 'inventoryManager/user_login_form.html', context)

    return render(request, 'inventoryManager/user_login_form.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('index')

def UserDetails(request):
    context = {}

    # user authenticated specific stuff
    if request.user.is_authenticated:
        # User's logged in, so we get their object
        # and let them in
        context['currentuser'] = request.user
    else:
        # user's anonymous, so we can't show them a user page
        # let them know by bringing them to the login page.
        return redirect('login-user')

    context = {"currentuser" : request.user}
    return render(request, 'inventoryManager/user_details.html', context)

# ///////////////////////////////////////////////
# //       END OF USER SPECIFIC STUFF          /////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////

# ///////////////////////////////////////////////
# //     BEGIN ORGANIZATION SPECIFIC STUFF     /////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////

# Method to create an organization
def CreateOrganization(request):
    form = OrganizationForm()
    context = {}

    # user authenticated specific stuff
    if request.user.is_authenticated:
        # User's logged in, so we get their object
        # and let them in
        context['currentuser'] = request.user
    else:
        # user's anonymous, so we can't let them make an organization
        # let them know by bringing them to the login page.
        return redirect('login-user')

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
                   about = data['about'],
                   associatedUser = request.user
                   )

               #commit new object to database
               newOrganization.save()

               # Redirect back to the organizations list page
               return redirect('organizations')

    context['form'] = form
    context['state'] = "Create"
    return render(request, 'inventoryManager/organization_form.html', context)

# Method to edit an organization
def EditOrganization(request, id):
    organizationToUpdate = Organization.objects.get(pk=id)
    context = {'organization' : organizationToUpdate}

    # user authenticated specific stuff
    if request.user.is_authenticated and organizationToUpdate.associatedUser == request.user:
        # User's logged in, so we get their object. we also check if this is their organization
        # and let them in
        context['currentuser'] = request.user
        context['allow'] = 'yes'
    elif request.user.is_authenticated and organizationToUpdate.associatedUser != request.user:
        # this isn't the user's organization. can't let them do poking now can we?
        # don't let them edit anything and redirect to permission denied page since they probably
        # poked around to get here
        context['currentuser'] = request.user
        return render(request, 'inventoryManager/denied.html')
    else:
        # user's anonymous, so we can't let them continue
        # let them know by bringing them to the login page.
        return redirect('login-user')

    # Populate the form with the organization's current data
    form = OrganizationForm(
        initial={"name" : organizationToUpdate.name,
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
               organizationToUpdate.about = data['about']

               #commit new object to database
               organizationToUpdate.save()

               # Redirect back to the organizations list page
               return redirect('organizations')

    context['form'] = form
    context['state'] = "Edit"
    return render(request, 'inventoryManager/organization_form.html', context)

# Method to delete an organization
def DeleteOrganization(request, id):
    # Get the data for the project to delete
    organizationToDelete = Organization.objects.get(id=id)
    context = {"organization" : organizationToDelete,
               'state' : "Delete"}

    # user authenticated specific stuff
    if request.user.is_authenticated and organizationToDelete.associatedUser == request.user:
        # User's logged in, so we get their object. we also check if this is their organization
        # and let them in
        context['currentuser'] = request.user
        context['allow'] = 'yes'
    elif request.user.is_authenticated and organizationToDelete.associatedUser != request.user:
        # this isn't the user's organization. can't let them do poking now can we?
        # don't let them delete stuff and redirect to permission denied page since they probably
        # poked around to get here
        context['currentuser'] = request.user
        return render(request, 'inventoryManager/denied.html')
    else:
        # user's anonymous, so we can't let them continue
        # let them know by bringing them to the login page.
        return redirect('login-user')

    if (request.method == 'POST' and organizationToDelete != None):
        if request.POST['submit'] == "Cancel":
            # User changed mind, redirect back to the project detail page
            return redirect('organization-detail', id)
        elif request.POST['submit'] == "Delete":
            organizationToDelete.delete()
            return redirect('organizations')

    return render(request, 'inventoryManager/organization_delete.html', context)

# Organization detail view
def OrganizationDetailView(request, id):
    organization_id = id
    organization = Organization.objects.get(pk=organization_id)
    context = {'organization' : organization}

    # user authenticated specific stuff
    if request.user.is_authenticated and organization.associatedUser == request.user:
        # User's logged in, but we also want to make sure this is their organization
        context['currentuser'] = request.user
        context['allow'] = 'yes'


    orders = Order.objects.filter(organization = organization)
    context['order_list'] = orders

    return render( request, 'inventoryManager/organization_detail.html', context)

# Organization list view
def OrganizationListView(request):
    organization_list = Organization.objects.all()
    context = {}

    # user authenticated specific stuff
    if request.user.is_authenticated:
        # User's logged in, go get their username
        # also, we want the template to be slightly different, but that's on the template side
        context['currentuser'] = request.user
        context['allow'] = 'yes'
        # first we want to get the user's organizations
        usersOrgs = Organization.objects.all().filter(associatedUser=request.user)
        context['usersOrgs'] = usersOrgs
        #now we want to get organizations that aren't the user's
        notUsersOrgs = []
        for org in organization_list:
            if org.associatedUser != request.user:
                notUsersOrgs.append(org)
        context['notUsersOrgs'] = notUsersOrgs

    context['organization_list'] = organization_list
    return render( request, 'inventoryManager/organization_list.html', context)

# ///////////////////////////////////////////////
# //    END OF ORGANIZATION SPECIFIC STUFF     /////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////

# ///////////////////////////////////////////////
# //         BEGIN ORDER SPECIFIC STUFF        /////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////

# Method to create an order
def OrganizationCreateOrder(request, id):
    organization_id = id
    form = OrderForm()
    organization = Organization.objects.get(pk=organization_id)
    context = {}

    # user authenticated specific stuff
    if request.user.is_authenticated and organization.associatedUser == request.user:
        # User's logged in, so we get their object. we also check if this is their organization
        # and let them in
        context['currentuser'] = request.user
        context['allow'] = 'yes'
    elif request.user.is_authenticated and organization.associatedUser != request.user:
        # this isn't the user's organization. how did they get this far?
        # sounds like someone with too much time on their hands
        # don't let them mess with this organization
        context['currentuser'] = request.user
        return render(request, 'inventoryManager/denied.html')
    else:
        # user's anonymous, so we can't let them continue
        # let them know by bringing them to the login page.
        return redirect('login-user')

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

    context['form'] = form
    context['organization'] = organization
    context['state'] = "Create"
    return render(request, 'inventoryManager/order_form.html', context)

# Method to edit an order
def OrganizationEditOrder(request, orgId, orderId):
    organization = Organization.objects.get(pk=orgId)
    orderToEdit = Order.objects.get(pk=orderId)
    context = {'order' : orderToEdit}

    # prefill form with existing data
    form = OrderForm(
        initial={"title" : orderToEdit.title,
                 "description" : orderToEdit.description,
                 "posted" : orderToEdit.posted,
                 "ordered" : orderToEdit.ordered,
                 "completed" : orderToEdit.completed,
                 }
        )

    # user authenticated specific stuff
    if request.user.is_authenticated and organization.associatedUser == request.user:
        # User's logged in, so we get their object. we also check if this is their organization
        # and let them in
        context['currentuser'] = request.user
        context['allow'] = 'yes'
    elif request.user.is_authenticated and organization.associatedUser != request.user:
        # this isn't the user's organization. can't let them do mischief can we?
        # seriously, the bum who decides to poke around with other people's things
        # should get a writeup.
        # TODO add something to log users doing naughty stuff, I swear.
        context['currentuser'] = request.user
        return render(request, 'inventoryManager/denied.html')
    else:
        # user's anonymous, so we can't let them continue
        # let them know by bringing them to the login page.
        return redirect('login-user')

    if (request.method == 'POST'):
        if request.POST['submit'] == "Cancel":
            return redirect('order-detail', orgId, orderId)
        elif request.POST['submit'] == "Submit":
            # Get form data and verify
            form = OrderForm(request.POST.copy())

            if form.is_valid():
                #clean the form data and assign it to something we can use
                data = form.cleaned_data
                
                orderToEdit.posted = data['posted']
                orderToEdit.ordered = data['ordered']
                orderToEdit.completed = data['completed']
                orderToEdit.title = data['title']
                orderToEdit.description = data['description']

                #commit the order to database
                orderToEdit.save()

                # Redirect back to the portfolio detail page
                return redirect('order-detail', orgId, orderId)

    context['form'] = form
    context['organization'] = organization
    context['state'] = "Edit"
    return render(request, 'inventoryManager/order_form.html', context)

# Method to delete an order
def OrganizationDeleteOrder(request, orgId, orderId):
    # Get the data for the order to delete
    orderToDelete = Order.objects.get(id=orderId)
    context = {"order" : orderToDelete,
               'organization' : orderToDelete.organization,
               'state' : 'Delete'}

    # user authenticated specific stuff
    if request.user.is_authenticated and orderToDelete.organization.associatedUser == request.user:
        # User's logged in, so we get their object. we also check if this is their organization
        # and let them in
        context['currentuser'] = request.user
        context['allow'] = 'yes'
    elif request.user.is_authenticated and orderToDelete.organization.associatedUser != request.user:
        # this isn't the user's organization. okay at this point whoever keeps fucking with stuff
        # needs to get a life. unless we hired that one to poke.
        context['currentuser'] = request.user
        return render(request, 'inventoryManager/denied.html')
    else:
        # user's anonymous, so we can't let them continue
        # let them know by bringing them to the login page.
        return redirect('login-user')

    if (request.method == 'POST' and orderToDelete != None):
        if request.POST['submit'] == "Cancel":
            # User changed mind, redirect back to the order detail page
            return redirect('order-detail', orgId, orderId)
        elif request.POST['submit'] == "Delete":
            # delete and go to the organization
            orderToDelete.delete()
            return redirect('organization-detail', orgId)

    return render(request, 'inventoryManager/order_delete.html', context)

# ORDER DETAIL METHOD
def OrderDetailView(request, organizationId, orderId):
    order = Order.objects.get(pk=orderId)
    organization = Organization.objects.get(pk=organizationId)
    context = {
                'order' : order,
                'organization' : order.organization
        }

    # user authenticated specific stuff
    if request.user.is_authenticated and organization.associatedUser == request.user:
        # User's logged in, so we get their object. we also check if this is their organization
        # and let them in
        context['currentuser'] = request.user
        context['allow'] = 'yes'
    elif request.user.is_authenticated and organization.associatedUser != request.user:
        # this isn't the user's organization. this is literally the same stuff, i should probably add this to a function
        context['currentuser'] = request.user
        return render(request, 'inventoryManager/denied.html')
    else:
        # user's anonymous, so we can't let them continue
        # let them know by bringing them to the login page.
        return redirect('login-user')

    itemsInOrder = OrderItem.objects.filter(order = order)
    context['item_list'] = itemsInOrder

    return render(request, 'inventoryManager/order_detail.html', context)

# ///////////////////////////////////////////////
# //         END OF ORDER SPECIFIC STUFF       /////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////

# Method to create an order item
def CreateOrderItem(request, organizationId, orderId):
    order = Order.objects.get(pk=orderId)
    organization = order.organization

    context = {'order' : order,
               'organization' : organization,
               'state' : "Create"
               }
    context['form'] = OrderItemForm()

    # user authenticated specific stuff
    if request.user.is_authenticated and organization.associatedUser == request.user:
        # User's logged in, so we get their object. we also check if this is their organization
        # and let them in
        context['currentuser'] = request.user
        context['allow'] = 'yes'
    elif request.user.is_authenticated and organization.associatedUser != request.user:
        # this isn't the user's organization. holy crap
        # however the banshee or something got to figure out how to get here is a real piece of work
        # by this point I should congratulate them for getting this far.
        context['currentuser'] = request.user
        return render(request, 'inventoryManager/denied.html')
    else:
        # user's anonymous, so we can't let them continue
        # let them know by bringing them to the login page.
        return redirect('login-user')

    if (request.method == 'POST'):
        if request.POST['submit'] == "Cancel":
            # user canceled, bring them back to the order detail page
            return redirect('order-detail', organization.id, order.id)
        elif request.POST['submit'] == "Submit":
            # Get form data and verify
            item_data = request.POST.copy()
        
            form = OrderItemForm(item_data)
            if form.is_valid():
                #clean the form data and assign it to something we can use
                data = form.cleaned_data

                newOrderItem = OrderItem(
                    itemName = data['itemName'],
                    itemNsn = data['itemNsn'],
                    itemQuantity = data['itemQuantity'],
                    itemCost = data['itemCost'],

                    order = order,
                    )

                #commit the order to database
                newOrderItem.save()

                # Redirect back to the order detail page
                return redirect('order-detail', organization.id, order.id)
    
    return render(request, 'inventoryManager/order_item_form.html', context)

# Method to edit an order item
def EditOrderItem(request, organizationId, orderId, itemId):
    order = Order.objects.get(pk=orderId)
    organization = order.organization
    itemToEdit = OrderItem.objects.get(pk=itemId)

    context = {'order' : order,
               'organization' : organization,
               'item_data' : itemToEdit,
               'state' : "Edit"
               }

    # user authenticated specific stuff
    if request.user.is_authenticated and organization.associatedUser == request.user:
        # User's logged in, so we get their object. we also check if this is their organization
        # and let them in
        context['currentuser'] = request.user
        context['allow'] = 'yes'
    elif request.user.is_authenticated and organization.associatedUser != request.user:
        # this isn't the user's organization. i'm done
        context['currentuser'] = request.user
        return render(request, 'inventoryManager/denied.html')
    else:
        # user's anonymous, so we can't let them continue
        # let them know by bringing them to the login page.
        return redirect('login-user')

    # prefill form with existing data
    context['form'] = OrderItemForm(
            initial={
                "itemName" : itemToEdit.itemName,
                "itemNsn" : itemToEdit.itemNsn,
                "itemQuantity" : itemToEdit.itemQuantity,
                "itemCost" : itemToEdit.itemCost,
                }
        )

    if (request.method == 'POST'):
        if request.POST['submit'] == "Cancel":
            # user canceled, bring them back to the order detail page
            return redirect('order-item-detail', organization.id, order.id, itemToEdit.id)
        elif request.POST['submit'] == "Submit":
            # Get form data and verify
            form = OrderItemForm(request.POST.copy())

            if form.is_valid():
                #clean the form data and assign it to something we can use
                data = form.cleaned_data

                itemToEdit.itemName = data['itemName']
                itemToEdit.itemNsn = data['itemNsn']
                itemToEdit.itemQuantity = data['itemQuantity']
                itemToEdit.itemCost = data['itemCost']

                #commit the order to database
                itemToEdit.save()

                # Redirect back to the order detail page
                return redirect('order-detail', organization.id, order.id)
    
    return render(request, 'inventoryManager/order_item_form.html', context)

# Method to delete an order item
def DeleteOrderItem(request, orgId, orderId, itemId):
    # Get the data for the order to delete
    itemToDelete = OrderItem.objects.get(id=itemId)
    order = Order.objects.get(pk=orderId)
    organization = order.organization
    context = {"item_data" : itemToDelete,
               'order' : order,
               'organization' : organization,
               'state' : "Delete"
               }

    # user authenticated specific stuff
    if request.user.is_authenticated and organization.associatedUser == request.user:
        # User's logged in, so we get their object. we also check if this is their organization
        # and let them in
        context['currentuser'] = request.user
        context['allow'] = 'yes'
    elif request.user.is_authenticated and organization.associatedUser != request.user:
        # this isn't under the user's organization. don't let them in
        context['currentuser'] = request.user
        return render(request, 'inventoryManager/denied.html')
    else:
        # user's anonymous, so we can't let them continue
        # let them know by bringing them to the login page.
        return redirect('login-user')

    if (request.method == 'POST' and itemToDelete != None):
        if request.POST['submit'] == "Cancel":
            # User changed mind, redirect back to the item detail page
            return redirect('order-item-detail', orgId, orderId, itemId)
        elif request.POST['submit'] == "Delete":
            # delete and go to the organization
            itemToDelete.delete()
            return redirect('order-detail', orgId, orderId)

    return render(request, 'inventoryManager/item_delete.html', context)

# Order item details method
def OrderItemDetail(request, organizationId, orderId, itemId):
    order = Order.objects.get(pk=orderId)
    organization = order.organization
    orderItem = OrderItem.objects.get(pk=itemId)
    context = {'order' : order,
               'organization' : organization,
               'orderItem' : orderItem}

    if request.user.is_authenticated and organization.associatedUser == request.user:
        # User's logged in, so we get their object. we also check if this is their organization
        # and let them in
        context['currentuser'] = request.user
        context['allow'] = 'yes'
    elif request.user.is_authenticated and organization.associatedUser != request.user:
        # this isn't under the user's organization.
        context['currentuser'] = request.user
        return render(request, 'inventoryManager/denied.html')
    else:
        # user's anonymous, so we can't let them continue
        # let them know by bringing them to the login page.
        return redirect('login-user')

    return render(request, 'inventoryManager/item_detail.html', context)