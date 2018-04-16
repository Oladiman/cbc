from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.utils.text import slugify
from django.db.models.signals import pre_save

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
    seller = models.ForeignKey(User, related_name='selling', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=120, choices=CATEGORY_CHOICES, default='11')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    negotiable = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_pic')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    state = models.CharField(max_length=30, null=True)
    campus = models.CharField(max_length=50, null=True)
    selling_type = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name
    
    def save(self):
        #Opening the uploaded image
        im = Image.open(self.image)

        output = BytesIO()

        #Resize/modify the image
        im = im.resize( (208,183) )

        #after modifications, save it to the output
        im.save(output, format='JPEG', quality=100)
        output.seek(0)

        #change the imagefield value to be the newley modifed image value
        self.img = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(Product,self).save()

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

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_product')
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product.name