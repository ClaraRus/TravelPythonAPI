from django.conf.urls import url
from django.contrib.auth import admin
from django.urls import include, path
from rest_framework import routers
from . import views
from .models import Tags

router = routers.DefaultRouter()
#router.register(r'tags', views.TagsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #path('api/', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^admin/', admin.site.urls),
    #url(r'^gettags/text=(?P<text>)(?s).*/$', views.gettags)
    url(r'^gettags/$', views.gettags),
    url(r'^getactivities/$', views.getactivities),
    url(r'^getfinalresult/$', views.getfinalresult),
    url(r'^getparagraphs/$', views.getparagraphs)

]