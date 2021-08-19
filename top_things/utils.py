from io import BytesIO
from django.core.files import File
from PIL import Image
import os
from datetime import datetime


# Resize image
def resize_image(image, size=(926, 617)):
    """Resize image of thing"""

    im = Image.open(image)
    im.convert('RGB')
    im.thumbnail(size)
    thumb_io = BytesIO()
    im.save(thumb_io, 'JPEG', quality=85)
    thumbnail = File(thumb_io, name=image.name)
    return thumbnail


# Select path and change name of uploaded image
def path_and_rename(instance, filename):
    """Select Path and Change name of image"""

    upload_to = 'things'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(datetime.now(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


# Validate parameter in filtering
def is_valid_queryparam(param):
    return param != '' and param is not None
