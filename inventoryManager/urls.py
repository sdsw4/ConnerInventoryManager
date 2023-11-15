from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path('createUser/', views.CreateUser, name = 'create-user'),
    path('login/', views.LoginUser, name = 'login-user'),
    path('logout/', views.LogoutUser, name = 'logout-user'),
    path('user/', views.UserDetails, name = 'user-details'),

    path('organizations/', views.OrganizationListView, name = 'organizations'),
    path('organization/<int:id>', views.OrganizationDetailView,
         name='organization-detail'),
    path('createOrganization/', views.CreateOrganization, name='create-organization'),
    path('editOrganization/<int:id>', views.EditOrganization,
         name='edit-organization'),
    path('deleteOrganization/<int:id>', views.DeleteOrganization,
         name='delete-organization'),

    path('organization/<int:id>/createOrder', views.OrganizationCreateOrder, name = 'create-order'),
    path('organization/<int:orgId>/editOrder/<int:orderId>', views.OrganizationEditOrder, name = 'edit-order'),
    path('organization/<int:orgId>/deleteOrder/<int:orderId>', views.OrganizationDeleteOrder, name = 'delete-order'),
    path('organization/<int:organizationId>/orders/<int:orderId>', views.OrderDetailView, name='order-detail'),

    path('organization/<int:organizationId>/orders/<int:orderId>/item/<int:itemId>', views.OrderItemDetail, name='order-item-detail'),
    path('organization/<int:organizationId>/orders/<int:orderId>/createOrderItem', views.CreateOrderItem, name='create-order-item'),
    path('organization/<int:organizationId>/orders/<int:orderId>/editItem/<int:itemId>', views.EditOrderItem, name='edit-order-item'),
    path('organization/<int:orgId>/orders/<int:orderId>/deleteItem/<int:itemId>', views.DeleteOrderItem, name='delete-order-item'),
]
