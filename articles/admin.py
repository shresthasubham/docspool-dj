from django.contrib import admin
from .models import Article,Book,ConferenceArticle,GeneralArticle

# Register your models here.
admin.site.register(Article)
admin.site.register(Book)
admin.site.register(ConferenceArticle)
admin.site.register(GeneralArticle)
