from django.db import models
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField
import datetime
import uuid
from file_validator.models import DjangoFileValidator
from tinymce.models import HTMLField

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

    username = None
    USERNAME_FIELD = "email"
    email = models.EmailField(
        "Adresse email", unique=True
    )  # changes email to unique and blank to false
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS
    objects = UserManager()

    # our specific fields
    first_name = models.CharField("Prénom", max_length=100, blank=True)
    last_name = models.CharField("Nom de famille", max_length=100, blank=True)
    confirmed_account = models.BooleanField("compte confirmé", default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(
        blank=True,
        upload_to="photos/",
        validators=[
            DjangoFileValidator(
                libraries=[
                    "python_magic",
                    "filetype",
                ],  # => validation operations will be performed with python-magic and filetype libraries
                acceptable_mimes=[
                    "image/png",
                    "image/jpeg",
                    "image/jpg",
                    "image/webp",
                ],  # => The mimes you want the file to be checked based on.
                acceptable_types=["image"],
                max_upload_file_size=5242880,
            )
        ],  # => 5 MB
    )
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
    status = models.CharField(
        "Statut", max_length=2, choices=STATUS_CHOICES, default="ET"
    )
    # looking_for_internship = models.BooleanField("En recherche de stage", default=False)
    # enseignant_hida = models.BooleanField(default=False)
    post_bac = HTMLField("Études après le Bac", max_length=1000, blank=True)
    occupation = HTMLField("Emploi", max_length=1000, blank=True)
    contact_info_instagram = models.URLField("Adresse compte instagram", blank=True)
    contact_info_email = models.EmailField(
        "Adresse email de contact",
        blank=True,
    )
    contact_info_linkedin = models.URLField("Adresse profil linkedin", blank=True)
    contact_info_tel = PhoneNumberField("Numéro de téléphone", blank=True, region="FR")

    class Meta:
        ordering = ["last_name", "first_name"]
