from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.utils.text import slugify
from django.db.models.signals import pre_save, pre_delete
import cloudinary
from cloudinary.models import CloudinaryField

# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('1', 'Phone, Tablets and Computers'),
        ('2', 'Phone Accessories'),
        ('3', 'Clothings and Accessories    '),
        ('4', 'Electronics'),
        ('5', 'Artwork'),
        ('6', 'Health & Beauty'),
        ('7', 'Home materials and furniture'),
        ('8', 'Kid and Babies'),
        ('9', 'Hostel and Accommodation'),
        ('10', 'Jobs and Services'),
        ('11', 'Miscellaneous')
    )
#     STATE_CHOICES = (
#         ('1',	'ABIA'),
#         ('2',	'ADAMAWA'),
#         ('3',	'AKWA IBOM'),
#         ('4',	'ANAMBRA'),
#         ('5',	'BAUCHI'),
#         ('6',	'BAYELSA'),
#         ('7',	'BENUE'),
#         ('8',	'BORNO'),
#         ('9',	'CROSS RIVER'),
#         ('10',	'DELTA'),
#         ('11',	'EBONYI'),
#         ('12',	'EDO'),
#         ('13',	'EKITI'),
#         ('14',	'ENUGU'),
#         ('15',	'FCT'),
#         ('16',	'GOMBE'),
#         ('17',	'JIGAWA'),
#         ('18',	'KADUNA'),
#         ('19',	'KANO'),
#         ('20',	'KATSINA'),
#         ('21'	'KEBBI'),
#         ('22'   'KOGI'),
#         ('23'	'KWARA'),
#         ('24'	'LAGOS'),
#         ('25'	'NIGER'),
#         ('26'	'NASSARAWA'),
#         ('27'	'OGUN'),
#         ('28'	'ONDO'),
#         ('29'	'OSUN'),
#         ('30'	'OYO'),
#         ('31'	'PLATEAU'),
#         ('32'	'RIVERS'),
#         ('33'	'SOKOTO'),
#         ('34'	'TARABA'),
#         ('35'	'YOBE'),
#         ('36'  'ZAMFARA')
# )
# CAMPUS_CHOICES=(
#    ( 'Gregory University'),
#   (  'America University of Nigeria'),
#   ( ' Akwa Ibom State University'),
#     ('Anambra State University'),
#    ( 'Abubakar Tafawa Balewa University'),
#    (' Benue State University'),
#    ( 'Cross River University of Technology'),
#   ( ' University of Calabar'),
#    (' Delta State University, Abraka'),
#     ('Michael and Cecilia Ibur University'),
#    (' Ebonyi State University'),
#    (' Ambrose Alli University'),
# (' Benson Idahosa University'),
#     ('Igbinedion University'),
#    ( 'University of Benin'),
#    (' Afe Babalola University'),
#    ( 'Ekiti State University'),
#    (' Federal University Oye'),
#    ( 'Federal polytechnic Ado'),
#    (' Caritas University'),
#    (' Godfrey Okoye University'),
#    (' University of Nigeria, Nsukka'),
#     ('University of Abuja'),
#    ( 'Nigerian Turkish Nile University'),
#   ( ' Veritas University(Catholic University of Nigeria)'),
#   ( ' Amadu Bello University'),
#   ( ' City Univerity of Technology'),
#   ( ' Bayero University'),
#   ( ' Fedral University, Dustin-Ma'),
#    ( 'Umaru Musa Yar’adua University'),
#    (' Kogi State University'),
#    (' University of Ilorin'),
#    ( 'Al-Hikmah University'),
#   ( ' Landmark University'),
#   ( ' CETEP City University),
#     ('Caleb University'),
#    (' City University'),
#   ( ' Lagos State University'),
#   ( ' University of Lagos'),
#    (' ECWA Bingham University'),
#    (' Babcock University'),
#    ( 'Bells University of Technology'),
#    (' Crawford University'),
#     ('Crescent University'),
#    (' Covenant University'),
#    (' Adekunle Ajasin University'),
#    (' Achievers University'),
#    ( 'Elizade University'),
#    (' Federal University of Technology Akure'),
#   ( ' Obafemi Awolowo University')
#    (' Joseph Ayo Babalola'),
#    (' Reedemers University'),
#    (' Bowen University'),
#    ( 'Fountain University'),
#    (' Oduduwa University'),
#    (' The Poly Ife'),
#    (' Ede Polytechnic'),
#    (' Ajayi Crowther University'),
#    (' Koladaisi University'),
#     ('University of Ibadan'),,
#    (' Ibadan Poly'),
#     ('University of Portharcourt'),
#    (' Taraba State University'),
#    (' Bukar Abba Ibrahim University'),
# )

    seller = models.ForeignKey(User, related_name='selling', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=120, choices=CATEGORY_CHOICES, default='11')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    negotiable = models.BooleanField(default=True)
    # image = models.ImageField(upload_to='product_pic')
    image = CloudinaryField('image')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    state = models.CharField(max_length=30, null=True)
    campus = models.CharField(max_length=50,null=True)
    selling_type = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name
    
    # def save(self):
    #     #Opening the uploaded image
    #     im = Image.open(self.image)

    #     output = BytesIO()

    #     #Resize/modify the image
    #     im = im.resize( (208,183) )

    #     #after modifications, save it to the output
    #     im.save(output, format='JPEG', quality=100)
    #     output.seek(0)

    #     #change the imagefield value to be the newley modifed image value
    #     self.img = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

    #     super(Product,self).save()

def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Product)

def photo_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.image.public_id)

pre_delete.connect(photo_delete, sender=Product)

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_product')
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product.name
