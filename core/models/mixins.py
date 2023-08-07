"""
Fly mixins
"""

from django.db import models
from django.utils import timezone


class DateTimeTrackMixin:
    """
    Mixin to automatically track the creation and last modification times
    of an object.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ------------------------------------------------------------
# SoftDeleteMixin
# ------------------------------------------------------------


class DeletedManager(models.Manager):
    """
    Manager to retrieve objects that have been soft deleted.
    Objects are considered soft deleted if the deleted_at field is not null.
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class ActiveManager(models.Manager):
    """
    Manager to retrieve objects that have not been soft deleted.
    Objects are considered active if the deleted_at field is null.
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class SoftDeleteMixin:
    """
    Mixin to provide soft delete functionality.
    Soft deleted objects are not removed from the database but are flagged as deleted.
    """

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects = ActiveManager()
    deleted_objects = DeletedManager()
    all_objects = models.Manager()

    def delete(self, *args, force=False, **kwargs):
        """
        Soft delete the object by setting the deleted_at field to the current time.
        If force=True, the object will be permanently removed from the database.
        """

        if force:
            return super().delete(*args, **kwargs)
        else:
            self.deleted_at = timezone.now()
            self.save()

    def restore(self):
        """
        Restore a soft deleted object by setting the deleted_at field to None.
        """
        
        self.deleted_at = None
        self.save()
