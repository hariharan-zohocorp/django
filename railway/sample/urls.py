from django.urls import path, re_path
from sample import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('pnr/', views.pnr, name='pnr'),
    path('book/', views.book, name='book'),
    path(r'^pnr/delete_passenger/<int:id>$',
         views.deleteAfter, name='deleteAfter'),
    path(r'^pnr/delete_ticket/<int:pnr>$', views.refund, name='delete'),
    path(r'^pnr/refund/<int:pnr>$', views.deleteTicket, name='deleteTicket'),
    path('create/', views.create, name='create'),
    path(r'^create/delete/<int:id>$', views.deleteIndividual,
         name='delete_individual'),
    path(r'^display/$', views.display, name='display')
]
