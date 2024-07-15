from django import forms
from client.models import Client, Address, ClientRelationship
from django.core.exceptions import ValidationError

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'id_number']

    def clean_id_number(self):
        id_number = self.cleaned_data['id_number']

        # Validate South African ID number format
        if not self.is_valid_sa_id(id_number):
            raise ValidationError("Invalid South African ID number format.")

        # Check if a client with the same ID number exists
        if Client.objects.filter(id_number=id_number).exists():
            raise ValidationError("A client with this ID number already exists.")

        return id_number

    def is_valid_sa_id(self, id_number):
        # Algorithms in client side    
        return True  

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['client']

class ClientRelationshipForm(forms.ModelForm):
    class Meta:
        model = ClientRelationship
        fields = ['client_to', 'relationship_type']

    client_from = forms.ModelChoiceField(queryset=Client.objects.all(), widget=forms.HiddenInput())
