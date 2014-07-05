from django.contrib import admin
from flashcard_app.models import Flashcard, FlashcardGroup
# Register your models here.

admin.site.register(Flashcard)
admin.site.register(FlashcardGroup)