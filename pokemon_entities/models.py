from django.db import models
from django.utils.timezone import localtime, now


class Pokemon(models.Model):
    title = models.CharField(max_length=100, verbose_name="Имя покемона")
    image = models.ImageField(blank=True, null=True,
                              verbose_name="Картинка покемона")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание")
    title_en = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Имя на английском")
    title_jp = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Имя на японском")
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name="Предыдущая эволюция"
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="entities",
        verbose_name="Покемон",
    )
    latitude = models.FloatField(verbose_name="Ширина")
    longitude = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(
        verbose_name="Появится в", null=True)
    disappeared_at = models.DateTimeField(
        verbose_name="Исчезнет в", null=True)
    level = models.IntegerField(verbose_name="Уровень", null=True, blank=True)
    health = models.IntegerField(
        verbose_name="Здоровье", null=True, blank=True)
    attack = models.IntegerField(verbose_name="Атака", null=True, blank=True)
    defense = models.IntegerField(
        verbose_name="Защита", null=True, blank=True)
    stamina = models.IntegerField(
        verbose_name="Стамина", null=True, blank=True)

    def __str__(self):
        return self.pokemon.title
