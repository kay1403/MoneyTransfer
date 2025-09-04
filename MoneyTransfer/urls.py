from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/', include('core.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/transactions/', include('transactions.urls')),
    path('api/auth/', include('accounts.urls')),
    path('api/', RedirectView.as_view(url='/api/core/', permanent=False)),
    path('', TemplateView.as_view(template_name='index.html')),
]
