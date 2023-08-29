from django.db import models
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField

import datetime
import uuid

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    "our custom User object, that doesn't use usernames"

    USERNAME_FIELD = "email"
    email = models.EmailField(
        "Adresse email", unique=True
    )  # changes email to unique and blank to false
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS
    objects = UserManager()

    # our specific fields
    confirmed_account = models.BooleanField("compte confirmé", default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(blank=True)
    bac_year = models.PositiveIntegerField(
        "Année du bac",
        default=datetime.date.today().year,
        validators=[validators.MinValueValidator(1984)],
    )

    STATUS_CHOICES = [
        ("ET", "Étudiant·e"),
        ("SA", "Salarié·e"),
        ("IN", "Indépendant·e"),
        ("EN", "En recherche"),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="ET")
    looking_for_internship = models.BooleanField("En recherche de stage", default=False)
    enseignant_hida = models.BooleanField(default=False)
    contact_info_instagram = models.URLField("Compte instagram", blank=True)
    contact_info_email = models.EmailField(
        "Adresse email de contact",
        blank=True,
    )
    contact_info_linkedin = models.URLField("Adresse profil linkedin", blank=True)
    contact_info_tel = PhoneNumberField(blank=True, region="FR")
