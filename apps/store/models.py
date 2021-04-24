from io import BytesIO
from django.core.files import File
from django.db import models

#PIL is Python Image Library and 'pillow' is its extension
from PIL import Image

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    ordering = models.IntegerField(default=0)

    class Meta:
        #describes the plural of class name 'category' to show in admin
        verbose_name_plural = 'categories'
        #orders the items according to given numbers (manual ordering)
        ordering = ('ordering',)
        
    def __str__(self):
        return f'category of {self.title}'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    is_featured = models.BooleanField(default=False)

    #Only 'JPEG' uploads, '.png' throws error
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True) #default=timezone.now

    class Meta:
        ordering = ('-date_added',) #ordering according to date added

    def __str__(self):
        return self.title

    #Custom Functions
    def save(self, *args, **kwargs):
        print('Save:', self.image.path)
        self.thumbnail = self.make_thumbnail(self.image)
        super().save(*args, **kwargs)

    def make_thumbnail(self, image, size=(350, 350)):
        """ Makes thumbnail of the uploaded Image """
        img = Image.open(image)
        img.convert("RGB")
        thumb = img.resize(size)

        thumb_io = BytesIO()
        #saving the image as '.jpg'
        thumb.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail