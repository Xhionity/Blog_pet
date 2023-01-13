from django.urls import path
from . import views
urlpatterns = [
	path('', views.home, name='blog-home'),
	path("edit/<int:id>", views.edit),
	path("delete/<int:id>", views.delete),
	path('<int:pk>/like/', views.AddLike.as_view(), name='like'),
	path('<int:pk>/dislike/', views.AddDislike.as_view(), name='dislike'),
]