import datetime
from django.db import models
from seeds.models import Seeds


#Farm's model with the atributes: user_id, farm_name, longitude and latitude
#Parcel's model with the atributes: farm_id, seed_id, width, length, crop_modality 
class Farm(models.Model):
    user_id = models.IntegerField(null = False, blank = False)
    farm_name = models.CharField(null = False, blank = False, max_length = 64)
    longitude = models.DecimalField(null = False, blank = False, max_digits=30, decimal_places=15)
    latitude = models.DecimalField(null = False, blank = False, max_digits=30, decimal_places=15)
    date_creation_farm = models.DateField(auto_now = True)

    #Create farm function to insert a new Farm into bd
    @classmethod
    def create_farm(cls, user_id, farm_name, longitude, latitude):
        farm = cls(user_id=user_id, farm_name=farm_name, latitude=latitude, longitude=longitude)
        farm.save()
        return farm
    
    def update_farm(self, data):
        farm_name = data.get('farm_name', None)
        longitude = data.get('longitude', None)
        latitude = data.get('latitude', None)
        self.farm_name = self.farm_name if not farm_name else farm_name
        self.longitude = self.longitude if not longitude else longitude
        self.latitude = self.latitude if not latitude else latitude
        self.save()
        return self


class Parcel(models.Model):
    """
    A Django model that represents a parcel of land.

    Fields:
    - farm_id: A foreign key to the Farm model, representing the farm to which the parcel belongs.
    - seed_id: A foreign key to the Seeds model, representing the seed used in the parcel.
    - width: The width of the parcel.
    - length: The length of the parcel.
    - crop_modality: The crop modality of the parcel, with choices of 'Outdoor' or 'Indoor'.
    - date_creation_parcel: The date of creation of the parcel.
    """

    CHOICES_CROP_MODALITY = (('Outdoor', 'Outdoor'), ('Indoor', 'Indoor'))

    farm = models.ForeignKey(Farm, on_delete=models.PROTECT)
    seed = models.ForeignKey(Seeds, on_delete=models.PROTECT)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    crop_modality = models.CharField(choices=CHOICES_CROP_MODALITY, max_length=30)
    date_creation_parcel = models.DateField(default=datetime.date.today)

    @classmethod
    def create_parcel(cls, farm_id: int, seed_id: int, width: float, length: float, crop_modality: str) -> 'Parcel':
        """
        Creates a new parcel with the given parameters and saves it to the database.

        Parameters:
        - farm_id: The farm ID of the parcel.
        - seed_id: The seed ID of the parcel.
        - width: The width of the parcel.
        - length: The length of the parcel.
        - crop_modality: The crop modality of the parcel.
        - date_creation_parcel: The date of creation of the parcel.

        Returns:
        - The created parcel.
        """
        parcel = cls(farm_id=farm_id, seed_id=seed_id, width=width, length=length, crop_modality=crop_modality)
        parcel.save()
        return parcel

    def update_parcel(self, data):
        seed = data.get('seed', None)
        width = data.get('width', None)
        length = data.get('length', None)
        crop_modality = data.get('crop_modality', None)
        if seed:
            self.seed = Seeds.objects.get(pk=seed)
        self.width = self.width if not width else width
        self.length = self.length if not length else length
        self.crop_modality = self.crop_modality if not crop_modality else crop_modality
        self.save()
        return self