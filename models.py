from tortoise import Model, fields


class FingerPrintModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    template=fields.TextField()
    def __str__(self):
        return self.name