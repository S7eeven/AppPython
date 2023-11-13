from django.shortcuts import render
import requests

def index(request):
    page_url = request.GET.get('page', 'https://pokeapi.co/api/v2/pokemon?offset=0')
    response = requests.get(page_url)
    data = response.json()
    results = data.get('results', [])
    index = []
    
    for pokemon in results:
        # Obtener información adicional de cada Pokémon
        pokemon_url = pokemon['url']
        pokemon_response = requests.get(pokemon_url)
        pokemon_data = pokemon_response.json()
        abilities_count = len(pokemon_data['abilities'])
        sprite_url = pokemon_data['sprites']['front_default']

        # Agregar información adicional al Pokémon
        pokemon['abilities_count'] = abilities_count
        pokemon['sprite_url'] = sprite_url

        index.append(pokemon)


    context = {
        'index': results,
        'next_page': data.get('next'),
        'previous_page': data.get('previous'),
    }
    return render(request, 'main/index.html', context)

def pokemon_detail(request, pokemon_name):
    api_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    response = requests.get(api_url)
    data = response.json()
    
    context = {
        'pokemon_data': data,
    }
    return render(request, 'main/pokemon_detail.html', context)

def search_pokemon(request):
    if request.method == 'GET':
        pokemon_name = request.GET.get('pokemon-search', '').strip()
        if pokemon_name:
            api_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/'
            response = requests.get(api_url)
            if response.status_code == 200:
                pokemon_data = response.json()
                abilities_count = len(pokemon_data['abilities'])
                sprite_url = pokemon_data['sprites']['front_default']

                context = {
                    'pokemon_data': pokemon_data,
                    'abilities_count': abilities_count,
                    'sprite_url': sprite_url,
                }
                return render(request, 'main/pokemon_detail.html', context)
            else:
                error_message = "Pokémon no encontrados. Por favor revisa el nombre y prueba de nuevo."
                return render(request, 'main/index.html', {'error_message': error_message})

    return render(request, 'main/index.html', {})