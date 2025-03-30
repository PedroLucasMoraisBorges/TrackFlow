from django.db import models
import uuid
import os

doc_types = [
    ('image', 'Imagem'),
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
    name = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Primeiro salva o arquivo
        if self.file and not self.name:
            self.name = os.path.basename(self.file.name)  # Define o nome sem "files/"
            super().save(update_fields=["name"]) 