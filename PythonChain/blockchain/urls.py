from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'get_chain', views.get_chain, basename='get_chain')
router.register(r'mine_block', views.mine_block, basename='mine_block')
router.register(r'is_valid', views.is_valid, basename='is_valid')
router.register(r'add_transaction', views.add_transaction, basename='add_transactions')
router.register(r'get_pending_transactions', views.get_pending_transactions, basename='get_pending_transactions')
router.register(r'connect_node', views.connect_node, basename='connect_node')
router.register(r'replace_chain', views.replace_chain, basename='replace_chain')
app_name = 'blockchain'
urlpatterns = [
    path('', include(router.urls)),
]