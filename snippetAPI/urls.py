
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from django.urls import path
from .views import *

urlpatterns = [

    path('registration/',RegistrationView.as_view(), name='registration'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('overview', OverViewAPI.as_view(), name='overview'),

    path('snippet_create/<str:id>', CreateAPI.as_view(), name='snippet_create'),
    path('snippet_details/<str:id>', DetailsAPI.as_view(), name='snippet_details'),
    path('snippet_update/<str:id>', UpdateAPI.as_view(), name='snippet_update'),
    path('snippet_delete/<str:id>', DeleteAPI.as_view(), name='snippet_delete'),

    path('tag_list/', TagListAPI.as_view(), name='tag_list'),
    path('tag_details/<str:id>', TagDetailsAPI.as_view(), name='tag_details'),
]