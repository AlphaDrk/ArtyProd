from audioop import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from django.views.generic import *
from .forms import  ProjectRequestForm, UserCreationForm
from django.contrib import messages
from .models import Client, Personnel, Projet, Service, Tache, Equipe
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import *
from django.contrib.auth.decorators import login_required


# Views for Personnel model
class PersHomeView(View):
    def get(self, request):
        personnel = Personnel.objects.all()
        projets = Projet.objects.all()
        services = Service.objects.all()
        taches = Tache.objects.all()
        equipes = Equipe.objects.all()
        client = Client.objects.all()

        context = {
            'personnel': personnel,
            'projets': projets,
            'services': services,
            'taches': taches,
            'equipes': equipes,
            'client': client,
        }
        return render(request, 'Personnel/PersDash.html', context)

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome {username}, your account has been created successfully!')
            return redirect('home')
        else:
            return render(request, 'registration/register.html', {'form': form})

class MyPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = '/password_reset/done/'

    def form_valid(self, form):
        # Override form_valid method to set the email to the user's email
        form.cleaned_data['email'] = self.get_user_email(form.cleaned_data['email'])
        return super().form_valid(form)

    def get_user_email(self, email):
        # Implement your logic to get the user's email based on the input email
        # This could involve querying your user model or any other method you use to store user emails
        # Return the user's email if found, or None if not found
        try:
            user = User.objects.get(email=email)
            return user.email
        except User.DoesNotExist:
            return None


def contact_user(request):
    if request.method == 'POST':
        sender_email = 'ArtyProd_Limited Company'
        recipient_email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)

    # Fetch the necessary data from the database
    personnel = Personnel.objects.all()
    projets = Projet.objects.all()
    services = Service.objects.all()
    taches = Tache.objects.all()
    equipes = Equipe.objects.all()
    client = Client.objects.all()

    context = {
        'personnel': personnel,
        'projets': projets,
        'services': services,
        'taches': taches,
        'equipes': equipes,
        'client': client,
    }

    # Pass the context data to the template
    return render(request, 'home.html', context)


class ContactUsView(TemplateView):
    template_name = 'home.html'

    def post(self, request, *args, **kwargs):
        # Process the form data and send the email
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        sender_email = request.POST.get('email')
        recipient_email = 'ArtyProd.Des@gmail.com'
        subject = request.POST.get('subject')
        message = f"👻 Name: {name}\n\n📞 Phone Number: {phone}\n\n📧 Email: {sender_email}\n\n📝 Message: {request.POST.get('message')}"

        send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)

        # Fetch the necessary data from the database
        personnel = Personnel.objects.all()
        projets = Projet.objects.all()
        services = Service.objects.all()
        taches = Tache.objects.all()
        equipes = Equipe.objects.all()
        client = Client.objects.all()

        context = {
            'personnel': personnel,
            'projets': projets,
            'services': services,
            'taches': taches,
            'equipes': equipes,
            'client': client,
        }

        # Pass the context data to the template
        return self.render_to_response(context)
    
class clientHomeView(View):
    def get(self, request):
        personnel = Personnel.objects.all()
        projets = Projet.objects.all()
        services = Service.objects.all()
        taches = Tache.objects.all()
        equipes = Equipe.objects.all()
        client = Client.objects.all()

        context = {
            'personnel': personnel,
            'projets': projets,
            'services': services,
            'taches': taches,
            'equipes': equipes,
            'client': client,
        }
        return render(request, 'Client/clientDash.html', context)

class HomeView(View):
    def get(self, request):
        personnel = Personnel.objects.all()
        projets = Projet.objects.all()
        services = Service.objects.all()
        taches = Tache.objects.all()
        equipes = Equipe.objects.all()
        client = Client.objects.all()

        context = {
            'personnel': personnel,
            'projets': projets,
            'services': services,
            'taches': taches,
            'equipes': equipes,
            'client': client,
        }
        
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context['is_admin'] = True
            elif personnel.filter(user=request.user).exists():
                context['is_personnel'] = True
            elif client.filter(user=request.user).exists():
                context['is_client'] = True

        return render(request, 'home.html', context)
    
@login_required
def myprofile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Retrieve additional user information or perform other operations
    # Pass the user object to the template context
    return render(request, 'client/myprofile.html', {'user': user})

@login_required
def update_profile(request, user_id):
    user = User.objects.get(id=user_id)
    client = user.client

    if request.method == 'POST':
        # Retrieve form data and update the user's information
        user.username = request.POST['username']
        user.email = request.POST['email']
        
        # Update other user information
        client.name = request.POST['name']
        client.address = request.POST['address']
        client.phone_number = request.POST['phone_number']
        
        # Handle image upload
        if 'image' in request.FILES:
            client.Img = request.FILES['image']
        
        user.save()
        client.save()
        
        # Redirect to the profile page after updating
        return redirect('myprofile', user_id=user.id)

    return render(request, 'client/myprofile.html', {'user': user, 'client': client})



@login_required
def myprojects_view(request):
    user = request.user
    client = get_object_or_404(Client, user=user)
    projects = Projet.objects.filter(clientP=client)
    project = None  # Initialize project as None
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Projet, id=project_id)
        # Retrieve form data and update the project's information
        project.libelle = request.POST['libelle']
        project.description = request.POST['description']
        # Update other project information
        project.save()
    return render(request, 'client/myproject.html', {'user': user, 'projects': projects, 'project': project})

@login_required
def update_project(request, project_id):
    project = get_object_or_404(Projet, id=project_id, clientP__user=request.user)

    if request.method == 'POST':
        # Retrieve the updated project information from the request parameters
        libelle = request.POST.get('libelle')
        description = request.POST.get('description')
        rate = request.POST.get('rate')

        # Update the project information if the values are provided
        if libelle:
            project.libelle = libelle
        if description:
            project.description = description
        if rate:
            project.rate = rate

        # Save the updated project
        project.save()

        # Redirect to the project list page after updating
        return redirect('myprojects')

    return render(request, 'client/myproject.html', {'project': project})


@login_required
def project_request_view(request):
    if request.method == 'POST':
        form = ProjectRequestForm(request.POST, request.FILES)
        if form.is_valid():
            project_request = form.save(commit=False)
            project_request.user = request.user
            project_request.save()
            return redirect('myprofile', user_id=request.user.id)
    else:
        form = ProjectRequestForm()

    return render(request, 'client/project_request.html', {'form': form})

@login_required
def project_request_list(request):
    project_requests = ProjectRequest.objects.filter(user=request.user)
    return render(request, 'client/rep_request.html', {'project_requests': project_requests})
