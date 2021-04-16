from django.db import models
from django.utils import timezone
from phone_field import PhoneField


class Property(models.Model):
    name=models.CharField(max_length=100,default="")
    url=models.CharField(max_length=100,default="")
    body=models.CharField(max_length=10000,default="")
    image_file = models.ImageField(upload_to='media', default='default.jpg')
    image_url = models.URLField(default='www.noimage.com')

    """def save(self, *args, **kwargs):
        get_remote_image(self)
        super().save(*args, **kwargs)  # Call the "real" save() method.
"""
    def __str__(self):
        return self.code

"""def get_remote_image(self):
    if self.image_url and not self.image_file:
        result = urllib.urlretrieve(self.image_url)
        self.image_file.save(
                os.path.basename(self.image_url),
                File(open(result[0]))
                )
        print('shieeett niga uploat')
        self.save()
"""
