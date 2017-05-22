"""nospammail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from nospammail import settings

def anonymous_required(function=None, home_url=None, redirect_field_name=None, custom_redirect=None):
    """Check that the user is NOT logged in.

    This decorator ensures that the view functions it is called on can be 
    accessed only by anonymous users. When an authenticated user accesses
    such a protected view, they are redirected to the address specified in 
    the field named in `next_field` or, lacking such a value, the URL in 
    `home_url`, or the `USER_HOME_URL` setting.
    """
    if home_url is None:
        home_url = settings.USER_HOME_URL

    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if request.user.is_authenticated():
                url = None
                if custom_redirect:
                    return custom_redirect
                if redirect_field_name and redirect_field_name in request.REQUEST:
                    url = request.REQUEST[redirect_field_name]
                if not url:
                    url = home_url
                if not url:
                    url = "/"
                return HttpResponseRedirect(url)
            else:
                return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)

urlpatterns = [
    url(r'^', include('settings_console.urls')),
    url(r'^login/$', anonymous_required(auth_views.login), name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/', include('login.urls')),
]

