from django.shortcuts import render
from django.views import View
from ArtyProd.models import Client, Equipe, Personnel, Projet, Service, Tache

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
        return render(request, 'home.html', context)