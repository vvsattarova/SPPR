from django.db import models


class Task(models.Model):
    title = models.CharField('Название', max_length=50, default='0')
    task = models.TextField('Описание', default='Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Prediction(models.Model):
    pred1 = models.TextField()
    pred2 = models.TextField()
    pred3 = models.TextField()
    pred4 = models.TextField()
    pred5 = models.TextField()
    pred6 = models.TextField()

    def __str__(self):
        return "Топ-6 аниме для выбранного пользователя"

    class Meta:
        verbose_name = 'Предсказание'
        verbose_name_plural = 'Предсказания'