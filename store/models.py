from django.db import models
from uuid import uuid4
from django.core.exceptions import ValidationError


def _new_image_path(instance, filename):
    """
    Rename image file and upload to
    'media/products/<product_sku>/<new_file_name>.<file_extension>'

    :param instance: the instance model name
    :param filename: name of actual file uploaded
    :return: String : <path>/<filename>.<extension>
    """

    file_extension = filename.rsplit('.', 1)[-1].lower()

    file_name = f'image_01.{file_extension}'
    path = f'products/{instance.sku}'

    return f'{path}/{file_name}'


def _new_product_files_path(instance, filename):
    """
    Rename product image's file to
    'media/products/<product_sku>/<new_file_name>.<file_extension>'

    :param instance: the instance model name
    :param filename: name of actual file uploaded
    :return: String : <path>/<filename>.<extension>
    """

    file_extension = filename.rsplit('.', 1)[-1].lower()

    file_name = f'{uuid4().hex}.{file_extension}'
    path = f'products/{instance.product.sku}'

    return f'{path}/{file_name}'


class Category(models.Model):
    """Simple Category model for Products"""

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=28)
    description = models.CharField(max_length=160, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name or self.name.isspace():
            raise ValidationError('Missing name')
        else:
            super().save(*args, **kwargs)


class Product(models.Model):
    """Products model for Store and Partners users"""

    class Meta:
        ordering = ('-date_version', 'name')

    name = models.CharField(max_length=80)
    sku = models.UUIDField(default=uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    description = models.TextField(max_length=999)
    date_version = models.DateField(auto_now_add=True)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to=_new_image_path)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name or self.name.isspace():
            raise ValidationError('Missing name')
        elif not self.description or self.description.isspace():
            raise ValidationError({'description': 'Missing description'})
        elif not self.base_price or self.base_price < 0.1:
            raise ValidationError(
                {'base_price': 'Please set a minimum price of 0.1'})
        else:
            super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Model for extra products images"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    image_name = models.CharField(max_length=32, blank=True, null=True)
    image = models.ImageField(upload_to=_new_product_files_path)

    def save(self, *args, **kwargs):
        """
        Override save method to give image file a default name based on
        products image count if no name given.
        Starts at 02 to avoid confusion with product's mandatory image_01 file.
        """

        if self.image_name is None:
            self.image_name = f'image_0{self.product.images.count() + 2}'

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.image_name} of {self.product.name} ' \
               f'#{self.product.sku}'


class Product3DFile(models.Model):
    """Model for Products 3D files"""

    product = models.OneToOneField(Product, on_delete=models.SET_NULL,
                                   related_name='printing_file',
                                   null=True, blank=True)
    file = models.FileField(upload_to=_new_product_files_path,
                            null=True, blank=True)

    def __str__(self):
        return f'{self.product.name} \'s printing file'
