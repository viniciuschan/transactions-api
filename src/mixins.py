from django.db import models
from django.utils import timezone

from .managers import SoftDeleteManager


class SoftDeleteModelMixin(models.Model):
    """Mixin model for soft delete."""

    deleted_at = models.DateTimeField(null=True)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def undelete(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

    def ultra_hard_delete(self):
        super().delete()
