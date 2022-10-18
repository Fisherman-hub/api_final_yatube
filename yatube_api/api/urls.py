from django.urls import include, path
from rest_framework import routers
from .views import CommentAPIView, FollowAPIView, GroupAPIView, PostAPIView

app_name = 'api'

router = routers.SimpleRouter()

router.register(r'posts', PostAPIView)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentAPIView, basename='comment')
router.register(r'groups', GroupAPIView)
router.register(r'follow', FollowAPIView, basename='follow')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
