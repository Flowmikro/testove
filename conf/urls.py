
from django.contrib import admin
from django.urls import path

from jsonrpc.views import JsonRpcView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', JsonRpcView.as_view(), name='jsonrpc_form'),
]
