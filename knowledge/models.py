from django.db import models


class Knowledge(models.Model):
    url = models.CharField(max_length=255)
    collection_id = models.UUIDField(primary_key=True)

    class Meta:
        db_table = "knowledge"
        managed = False
