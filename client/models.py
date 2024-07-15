from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    id_number = models.CharField(max_length=250,unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id_number})"

class Address(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    address_type_choices = (
        (0, "Physical"),
        (1, "Postal"),
    )
    address_type = models.IntegerField(
        choices=address_type_choices,
        default=0,
    )
    street = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
    )
    street_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    unit_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    building = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    area = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    province = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
    )

class ClientRelationship(models.Model):
    RELATIONSHIP_CHOICES = [
        ('Husband', 'Husband'),
        ('Wife', 'Wife'),
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
    ]
    
    client_from = models.ForeignKey(Client, related_name='relationships_from', on_delete=models.CASCADE)
    client_to = models.ForeignKey(Client, related_name='relationships_to', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES)
    
    class Meta:
        unique_together = ('client_from', 'client_to', 'relationship_type')
    
    def __str__(self):
        return f"{self.client_from} is {self.relationship_type} of {self.client_to}"
