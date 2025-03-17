from django.db import models
import uuid

doc_types = [
    ('img', 'Imagem'),
    ('pdf', 'PDF'),
    ('csv', 'CSV'),
    ('excel', 'Excel'),
    ('docx', 'Word (DOCX)'),
    ('txt', 'Texto (TXT)'),
    ('pptx', 'PowerPoint (PPTX)'),
    ('zip', 'Arquivo ZIP'),
]

# Create your models here.
class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='files')
    type = models.CharField(max_length=5, choices=doc_types, null=True)