from django.contrib.auth.models import User
from django.db import models

TYPE_STATUS = (
    (1, 'New'),
    (2, 'In Progress'),
    (3, 'In QA'),
    (4, 'Ready'),
    (5, 'Done')
)


class Card(models.Model):
    text = models.TextField()
    status = models.IntegerField(choices=TYPE_STATUS, default=1)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name='authors_cards', verbose_name='Автор', on_delete=models.CASCADE)
    executor = models.ForeignKey(User, related_name='executor_cards', verbose_name='Исполнитель',
                                 null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки'
