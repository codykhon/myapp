from .models import Receipts, Ingredients
from django.forms import ModelForm, TextInput, Textarea


class ReceiptForm(ModelForm):
    class Meta:
        model = Receipts
        exclude = ('author',)
        fields = [ "title" , "author", "patient"]
        widgets = {
            "title": TextInput(attrs={
                "class": 'form-control',
                'placeholder': 'Input Receipt Name',
                'aria-label':"Small",
                'aria-describedby':"inputGroup-sizing-sm",
            }),
        }
class IngredientForm(ModelForm):
    class Meta:
        model = Ingredients
        fields = [ "ingredient", "comments" ,"amount"]
        widgets = {
            "ingredient": TextInput(attrs={
                "class": 'form-control',
                'placeholder': 'Input ingredient name'
            }),
            "comments": Textarea(attrs={
                "class": 'form-control',
                'placeholder': 'Leave some comments'
            }),
        }