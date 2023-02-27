from django.urls import path
from .views import (PostList,
                    PostDetail,
                    PostSearch,
                    NewsCreate,
                    ArticlesCreate,
                    NewsUpdate,
                    ArticlesUpdate,
                    NewsDelete,
                    ArticlesDelete,
                    subscribe,
                    unsubscribe)


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('article/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('<int:pk>/news//update/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/article//update/', ArticlesUpdate.as_view(), name='articles_update'),
   path('<int:pk>/news/delete/', NewsDelete.as_view(), name='news_delete'),
   path('<int:pk>article/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   path('<int:pk>/subscribe/', subscribe, name='subscribe'),
   path('<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
]