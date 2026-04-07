from django.urls import path
from .views import MockProductsView, MockOrdersView, AccessRuleAdminView

urlpatterns = [
    path('products/', MockProductsView.as_view()),
    path('orders/', MockOrdersView.as_view()),
    path('rules/', AccessRuleAdminView.as_view()),
]