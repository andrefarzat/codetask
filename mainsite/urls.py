from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from mainsite.views import HomePageView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^$', HomePageView.as_view(), name='home'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
