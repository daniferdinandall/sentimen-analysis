from django.contrib import admin
from django.urls import path
from posting.views import *
from django.views.generic.base import RedirectView
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('riwayat/',riwayat,name='riwayat'),
    path('visual/',visual,name='visual'),
    path('visualRiwayat/<int:param>/',visualRiwayat,name='visualRiwayat'),
    path('remove/<int:param>/',remove,name='remove'),
    # path(r'^.*$', RedirectView.as_view(url='index', permanent=False), name='index')
]
