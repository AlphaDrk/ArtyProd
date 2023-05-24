from email.headerregistry import Group
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save

class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    skill = models.CharField(max_length=255, blank=True)
    ficher = models.FileField(upload_to='media/', blank=True)
    Img = models.ImageField(upload_to='media/', blank=True)
    lien_linkedIn = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        # Check if the user exists in the Client queryset
        if Client.objects.filter(user=self.user).exists():
            # Remove the user from the Client queryset
            client = Client.objects.get(user=self.user)
            client.delete()

        super().save(*args, **kwargs)
    def __str__(self):
        return f'  ➢  {self.nom}   💻  {self.skill}'

class Service(models.Model):
    TYPE_CHOICES = (
        ('Product Design', 'Product Design'),
        ('UX UI Design','UX UI Design'),
        ('Branding','Branding'),
        ('Digital Strategy','Digital Strategy'),
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField()
    Img = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return f'  ➢   {self.type}'

class Tache(models.Model):
    nom_tache = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='media/')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    projet = models.ForeignKey('Projet', on_delete=models.CASCADE, related_name='taches')
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)

    def __str__(self):
        return f'  ➢   {self.personnel}    💻   {self.projet}'

class Equipe(models.Model):
    nom = models.CharField(max_length=255)
    membres = models.ManyToManyField(Personnel)
    Img = models.ImageField(upload_to='media/', null=True, blank=True)
    
    def __str__(self):
        return f'  ➢  {self.nom}'
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    Img = models.ImageField(upload_to='media/', null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username}       🏫      {self.address}     📞      {self.phone_number}'
    
class Projet(models.Model):
    libelle = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    acheve = models.BooleanField(default=False)
    equipe = models.ForeignKey(Equipe, on_delete=models.PROTECT)
    clientP = models.ManyToManyField(Client, related_name='projets')
    TYPE_CHOICES = (
        ('★☆☆☆☆','★☆☆☆☆'),
        ('★★☆☆☆','★★☆☆☆'),
        ('★★★☆☆','★★★☆☆'),
        ('★★★★☆','★★★★☆'),
        ('★★★★★','★★★★★'),
    )
    rate = models.CharField(max_length=50, choices=TYPE_CHOICES,default=1)
    Img = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return f'   ➢   {self.libelle}   📆   {self.date_debut}   ⏰   {self.date_fin}'
 

@receiver(post_save, sender=User)
def create_client(sender, instance, created, **kwargs):
    if created:
        client = Client.objects.create(user=instance, address="", phone_number="")
        client_group = Group.objects.get(name='Client')
        client_group.user_set.add(instance)

class ProjectRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    company = models.CharField(max_length=100)
    project_type = models.CharField(max_length=100)
    project_description = models.TextField()
    ETAT_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    etat = models.CharField(max_length=15, choices=ETAT_CHOICES)
    file = models.FileField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return f'  ➢   {self.user}  📬  {self.email}   📞  {self.phone}    🌇    {self.company}    💻   {self.project_type}   ➢   {self.etat}'