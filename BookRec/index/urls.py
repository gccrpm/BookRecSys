from django.conf.urls import url

from index.views import home,login,history,switchuser,one

urlpatterns = [
    url(r'^home/$',home),
    url(r'^login/$',login),
    url(r'^history/$',history),
    url(r'^switchuser/$',switchuser),
    url(r'^one/$',one),
]