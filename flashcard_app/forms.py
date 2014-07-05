from django import forms
from flashcard_app.models import Flashcard, FlashcardGroup
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    #Hides the password as the user types it
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
        
class FlashcardGroupForm(forms.ModelForm):
    
    front_side = forms.CharField(label = "Front Side", max_length=50)
    back_side = forms.CharField(label = "Back Side", max_length=50)
    
    class Meta:
        model = FlashcardGroup
        fields = ('name', 'front_side', 'back_side')
        
class FlashcardForm(forms.ModelForm):
    
    class Meta:
        model = Flashcard
        fields = ('frontside', 'backside')
        
        