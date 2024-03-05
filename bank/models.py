from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password
from .constants import PROFILE_CHOICES

class Agency(models.Model):
    accounts = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=15, null=True)
    adress = models.CharField(max_length=255, null=True)
    agency_number = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)], unique=True)

    def __str__(self):
        return f"{self.accounts or 'Nenhuma conta foi criada'}"

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    profile = models.CharField(max_length=255, choices=PROFILE_CHOICES, default='undefined')

    def save(self, *args, **kwargs):
        if not self.pk:  # Apenas se for um novo objeto
            self.set_password(self.password)  # Define a senha ao salvar pela primeira vez
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    class Meta:
        # Defina as permissões do modelo aqui, se necessário
        permissions = [
            ("can_do_something", "Can do something"),
        ]

    # Adicione related_name aos campos groups e user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='custom_user_groups' 
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='custom_user_permissions' 
    )
    
class Clients(CustomUser):
   
    name = models.CharField(max_length=255)
    adress = models.CharField(max_length=255)
    client_email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=15)
    agency_id = models.ForeignKey(Agency, on_delete=models.CASCADE)
    account = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)], unique=True)
    date_birth = models.DateField()
    document = models.CharField(max_length=11, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    customuser_ptr = models.OneToOneField(CustomUser, on_delete=models.CASCADE, parent_link=True, related_name='client_customuser')
    def __str__(self):
        return f"{self.name} - {self.agency} - {self.account}"

class Colaborators(CustomUser):
    code = {
        ('C', 'Colaborator'),
        ('G', 'Gerente'),
    }
    name = models.CharField(max_length=255)

    phone = models.CharField(max_length=15)
    colaborator_email = models.EmailField(max_length=255)
    agency_id = models.ForeignKey(Agency, on_delete=models.CASCADE)
    registration = models.CharField(max_length=8, unique=True)
    date_birth = models.DateTimeField()
    document = models.CharField(max_length=11, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    nivel = models.CharField(max_length=1, choices=code, default='B')

    def __str__(self):
        return f'{self.name} - {self.get_nivel_display()}'
    

class Withdraw(models.Model):
    value= models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    user_id = models.ForeignKey(Clients, related_name='withdraws_by_user', null=False, on_delete=models.CASCADE)
    agency_id = models.ForeignKey(Agency, null=False, on_delete=models.CASCADE)
    account = models.ForeignKey(Clients, related_name='withdraws_by_account', null=False, on_delete=models.CASCADE, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Saque para {self.user_id.username} em {self.date_created}'

class Deposit(models.Model):
    value= models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    name = models.CharField(max_length=255, null=False)
    agency_id = models.ForeignKey(Agency, null=False, on_delete=models.CASCADE)
    account = models.ForeignKey(Clients, related_name='deposit_by_account', null=False, on_delete=models.CASCADE, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Deposito prar {self.user_id.account} em {self.date_created}'