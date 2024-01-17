from django import forms

from canteen.models import *

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
class ContactSubmissionForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'subject', 'message']

class EditCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']  # Include other fields if necessary