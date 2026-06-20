from django.urls import path
from .views import generate_post, post_history, toggle_favorite, generate_post_image, post_detail


urlpatterns = [
    path("generate/", generate_post, name="generate_post"),
    path("history/", post_history, name="post_history"),
    path("favorite/<int:pk>/", toggle_favorite, name="toggle_favorite"),
    path("generate-image/<int:post_id>/",generate_post_image,name="generate_post_image"),
    path("post/<int:post_id>/",post_detail, name="post_detail"),
    #path("generate-poster/<int:post_id>/",generate_poster,name="generate_poster"), 
    

]
