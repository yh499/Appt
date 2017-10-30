from django.conf.urls import url
from . import views          
urlpatterns = [

    url(r'^$', views.index),
    url(r'^regist$', views.regist),
    url(r'^login$', views.login),
    url(r'^appointments$', views.success),
    url(r'^logout$', views.logout),
    #works until you log in 
    url(r'^add$', views.add),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'appointments/(?P<id>\d+)$', views.edit),
    url(r'update$', views.update),

  
  ]

