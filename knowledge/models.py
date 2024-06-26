from django.db import models


class Knowledge(models.Model):
    account_id = models.IntegerField()
    url = models.CharField(max_length=255)
    collection_id = models.UUIDField(primary_key=True)

    class Meta:
        db_table = "knowledge"
        managed = False
