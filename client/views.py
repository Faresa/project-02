from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Client, ClientRelationship
from .forms import ClientForm, AddressForm, ClientRelationshipForm

class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('client_list')
        return super().get(request, *args, **kwargs)

class ClientList(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client_list.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(id_number__icontains=query)
            )

        return queryset

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "client_details.html"
    login_url = '/login/'

def create_client(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        address_form = AddressForm(request.POST)
        
        # Check if both forms are valid
        if client_form.is_valid() and address_form.is_valid():
            client = client_form.save(commit=False)
            address = address_form.save(commit=False)
            
            # Validate South African ID number format
            id_number = client.id_number
            if not is_valid_sa_id(id_number):
                client_form.add_error('id_number', 'Invalid South African ID number format.')
                return render(request, 'client_create.html', {'client_form': client_form, 'address_form': address_form})
            
            # Check uniqueness of ID number
            if Client.objects.filter(id_number=id_number).exists():
                client_form.add_error('id_number', 'This ID number already exists.')
                return render(request, 'client_create.html', {'client_form': client_form, 'address_form': address_form})
            
            client.save()
            address.client = client
            address.save()
            return redirect('client_list')
    else:
        client_form = ClientForm()
        address_form = AddressForm()
    
    return render(request, 'client_create.html', {'client_form': client_form, 'address_form': address_form})

def add_client_relationship(request, client_id):
    client_from = get_object_or_404(Client, pk=client_id)
    
    if request.method == 'POST':
        form = ClientRelationshipForm(request.POST)
        if form.is_valid():
            relationship = form.save(commit=False)
            relationship.client_from = client_from  # Assign client_from here
            relationship.save()
            
            # Create the inverse relationship
            inverse_relationship = ClientRelationship(
                client_from=relationship.client_to,
                client_to=relationship.client_from,
                relationship_type=get_inverse_relationship_type(relationship.relationship_type)
            )
            inverse_relationship.save()
            return redirect('client_list')
    else:
        form = ClientRelationshipForm(initial={'client_from': client_from})  # Pass client_from as initial data
    
    return render(request, 'add_client_relationship.html', {'form': form, 'client_from': client_from})

def get_inverse_relationship_type(relationship_type):
    inverse_relationships = {
        'Husband': 'Wife',
        'Wife': 'Husband',
        'Father': 'Daughter',
        'Mother': 'Son',
        'Son': 'Father',
        'Daughter': 'Mother',
        'Brother': 'Sister',
        'Sister': 'Brother'
    }
    return inverse_relationships.get(relationship_type, relationship_type)

def is_valid_sa_id(id_number):
    if len(id_number) != 13 or not id_number.isdigit():
        return False

    # Extract components from the ID number
    birth_date = id_number[:6]
    gender_code = int(id_number[6:10])
    citizenship = int(id_number[10])
    check_digit = int(id_number[12])

    return True
