from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet for soft deleted objects."""

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)

    def delete(self):
        return super().update(deleted_at=timezone.now())

    def undelete(self):
        return super().update(deleted_at=None)

    def ultra_hard_delete(self):
        return super().delete()


class SoftDeleteManager(models.Manager):
    """Custom manager for soft delete."""

    _queryset_class = SoftDeleteQuerySet

    def get_queryset(self):
        return super().get_queryset().alive()

    def deleteds(self):
        return super().get_queryset().dead()
