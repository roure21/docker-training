from django.db import models


class Author(models.Model):
    first_name = models.CharField('Nombre', max_length=30)
    last_name = models.CharField('Apellido', max_length=30)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'author'
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['last_name']


class Article(models.Model):
    headline = models.CharField('Titular', max_length=200)
    content = models.TextField('Contenido')
    author = models.ForeignKey(Author, verbose_name='Autor', on_delete=models.CASCADE)
    published_at = models.DateField('Fecha de Publicación')

    def __str__(self):
        return self.headline

    class Meta:
        db_table = 'article'
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        ordering = ['-published_at']
