import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime, now


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def get_photo_url(pokemon_image):
    return pokemon_image.url if pokemon_image else DEFAULT_IMAGE_URL


def show_all_pokemons(request):

    pokemons = Pokemon.objects.all()
    current_time = localtime(now())

    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in pokemon_entities:
        img_url = get_photo_url(entity.image)
        full_img_url = request.build_absolute_uri(img_url)
        add_pokemon(folium_map, entity.latitude,
                    entity.longitude, full_img_url)

    pokemons_on_page = []
    for pokemon in pokemons:
        img_url = get_photo_url(pokemon.image)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    current_time = localtime(now())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entitys = pokemon.entities.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
    )

    pokemon_details = {
        "img_url": get_photo_url(pokemon.image),
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
    }

    for entity in pokemon_entitys:
        img_url = get_photo_url(entity.pokemon.image)
        full_img_url = request.build_absolute_uri(img_url)
        add_pokemon(folium_map, entity.latitude,
                    entity.longitude, full_img_url)

    if pokemon.previous_evolution:
        pokemon_details["previous_evolution"] = {
            "title_ru": pokemon.previous_evolution.title,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": get_photo_url(pokemon.previous_evolution.image)
        }

    next_evolution = pokemon.next_evolutions.first()
    if next_evolution:
        pokemon_details["next_evolution"] = {
            "title_ru": next_evolution.title,
            "pokemon_id": next_evolution.id,
            "img_url": get_photo_url(next_evolution.image),
        }

    return render(request, 'pokemon.html', context={
        "map": folium_map._repr_html_(),
        "pokemon": pokemon_details,
    })
