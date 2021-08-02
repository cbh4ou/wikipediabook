from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class IndexedTimeStampedModel(models.Model):
    created = AutoCreatedField(_("created"), db_index=True)
    modified = AutoLastModifiedField(_("modified"), db_index=True)

    class Meta:
        abstract = True

class Wikis(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    cover_photo = models.ImageField(upload_to='chapter_covers')
    
