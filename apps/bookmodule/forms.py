from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'price', 'quantity', 'pubdate', 'rating', 'publisher', 'authors']

    # Example validation (optional)
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price
    
from .models import Student, Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'postal_code']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']

from .models import Student2, Address2

from django.forms import ModelMultipleChoiceField

class Student2Form(forms.ModelForm):
    addresses = forms.ModelMultipleChoiceField(
        queryset=Address2.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Student2
        fields = ['first_name', 'last_name', 'email', 'addresses']
from .models import ItemImage

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['title', 'image']
