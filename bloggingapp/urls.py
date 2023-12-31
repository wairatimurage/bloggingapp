from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin  # Import admin from django.contrib
from bloggingapp import settings
from gallery import views
from gallery.views import post_list

urlpatterns = [
                  path('', views.post_list, name='post_list'),
                  path('signin/', views.signin, name="signin"),
                  path('signout', views.signout, name="signout"),
                  path('post/<int:pk>/', views.post_detail, name='post_detail'),
                  path('search', views.search, name="search"),
                  path('posts/<str:category>/', post_list, name='post_list_filtered'),
                  path('post/new/', views.post_new, name='post_new'),
                  path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
                  path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
                  path('admin/', admin.site.urls),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
