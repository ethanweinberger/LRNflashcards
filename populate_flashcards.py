import os

def populate():
    
    weinbergere = User.objects.get(username = 'weinbergere')
    
    addFlashcardGroup("Test", weinbergere)
    addFlashcardGroup("Test2", weinbergere)
    addFlashcardGroup("Test3", weinbergere)
    
    
    test = FlashcardGroup.objects.get(name="Test")
    test2 = FlashcardGroup.objects.get(name="Test2")
    test3 = FlashcardGroup.objects.get(name="Test3")
    
    addFlashcard('front', 'back', test)
    addFlashcard('Je', 'I', test)
    addFlashcard('Il', 'He', test)
    addFlashcard('1', '2', test)
    addFlashcard('3', '4', test)
    addFlashcard('5', '6', test)
    addFlashcard('7', '8', test)
    addFlashcard('9', '10', test)
    addFlashcard('11', '12', test)
    addFlashcard('13', '14', test)
    addFlashcard('15', '16', test)
    addFlashcard('17', '18', test)
    
    addFlashcard('front', 'back', test2)
    addFlashcard('Je', 'I', test2)
    addFlashcard('Il', 'He', test2)
    
    addFlashcard('front', 'back', test3)
    addFlashcard('Je', 'I', test3)
    addFlashcard('Il', 'He', test3)
    

    print "Success!"
    
def addFlashcard(frontside, backside, group, active = True):
    f = Flashcard.objects.get_or_create(frontside = frontside, backside = backside, group = group, active = active)[0]
    return f

def addFlashcardGroup(name, user):
    g = FlashcardGroup.objects.get_or_create(name = name, user = user)[0]
    return g

if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flashcards.settings")
    from django.contrib.auth.models import User
    from flashcard_app.models import Flashcard, FlashcardGroup
    populate()
    

    
