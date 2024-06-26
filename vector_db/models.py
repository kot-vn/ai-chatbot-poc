from django.db import models


class Collection(models.Model):
    name = models.CharField(max_length=255)
    cmetadata = models.JSONField()
    uuid = models.UUIDField(primary_key=True)

    class Meta:
        db_table = "langchain_pg_collection"
        managed = False


class Embeddings(models.Model):
    collection_id = models.UUIDField()
    embedding = models.CharField(max_length=255)
    document = models.CharField(max_length=255)
    cmetadata = models.JSONField()
    custom_id = models.CharField(max_length=255)
    uuid = models.UUIDField(primary_key=True)

    class Meta:
        db_table = "langchain_pg_embedding"
        managed = False
