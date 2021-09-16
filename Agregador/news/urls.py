from django.urls import path
from django.urls.conf import include
from news.views import scrape, news_list
urlpatterns = [
  path('', news_list, name="home"),
  path('/scrap', scrape, name="scrape"),
] 