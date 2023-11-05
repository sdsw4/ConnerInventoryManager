from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path('organizations/', views.OrganizationListView, name = 'organizations'),
    path('organization/<int:id>', views.OrganizationDetailViewEx,
         name='organization-detail'),
    path('createOrganization/', views.CreateOrganization, name='create-organization'),
    path('editOrganization/<int:id>', views.EditOrganization,
         name='edit-organization'),
    path('deleteOrganization/<int:id>', views.DeleteOrganization,
         name='delete-organization'),

    path('organization/<int:id>/createOrder', views.OrganizationCreateOrder, name = 'create-order'),
    path('organization/<int:organizationId>/orders/<int:orderId>', views.OrderDetailView, name='order-detail'),
]
