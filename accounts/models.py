from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    AGENT = 'AGENT', 'Agent'          # personne qui valide / envoie Mobile Money
    CLIENT = 'CLIENT', 'Client'        # utilisateur final


class User(AbstractUser):
    """
    Custom User basé sur AbstractUser pour rester simple (pas besoin de manager custom).
    On ajoute téléphone, pays, rôle et un flag de vérification KYC.
    """
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    country = models.CharField(max_length=64, blank=True)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.CLIENT)
    is_kyc_verified = models.BooleanField(default=False)

    # Conseillé pour éviter les collisions d'email null vs unique
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
