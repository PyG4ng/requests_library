import requests

API_KEY = '2619421814940190'


class Superhero:
    def __init__(self, name):
        self.name = name
        self.hero_id = self._get_hero_id()
        self.intelligence = self._get_intelligence()

    def __str__(self):
        return f'{self.name}\nId: {self.hero_id}\nIntelligence: {self.intelligence}'

    def _get_hero_id(self):
        print(f'\nFetching for {self.name} id')
        response = requests.get(f'https://superheroapi.com/api/{API_KEY}/search/{self.name}')
        response.raise_for_status()
        if response.status_code == 200 and response.json().get('response') == "success":
            if len(response.json().get("results")) == 1:
                return response.json().get('results')[0].get('id')

            # If there is more than one result with the same name
            elif len(response.json().get("results")) > 1:
                print(f"More than 1 result for {self.name}")
                all_names_results = []
                for result in response.json().get("results"):
                    all_names_results.append(result.get("name"))
                print(f'Results for {self.name}')
                for ind, name in enumerate(all_names_results, 1):
                    print(f'{ind}.{name}')
                n = 0
                while n not in [str(num) for num in range(1, len(all_names_results) + 1)]:
                    n = input(
                        f"Choose the superhero you're looking for, integer between 1 and {len(all_names_results)}: ")
                self.name = response.json().get('results')[int(n) - 1].get('name')
                return response.json().get('results')[int(n) - 1].get('id')
        else:
            print(f'{self.name} not found!')
            return None

    def _get_intelligence(self):
        if self.hero_id is not None:
            print(f'Fetching for {self.name} intelligence')
            response = requests.get(f'https://superheroapi.com/api/{API_KEY}/{self.hero_id}/powerstats')
            if response.json().get('intelligence') != 'null':
                return int(response.json().get('intelligence'))
            print(f'No data for {self.name} intelligence! ')
        return None


def get_superhero_intelligence_powerstats(superheroes):
    """
    Takes superhero names and return a sorted list by intelligence powerstat

    Args:
        superheroes (list): Superhero names

    Returns: Superhero sorted list by intelligence

    """
    all_heroes = []
    for hero in superheroes:
        superhero = Superhero(hero)
        if superhero.intelligence is not None:
            all_heroes.append(superhero)
    return sorted(all_heroes, key=lambda p: p.intelligence, reverse=True)


def get_smartest_superhero(superheroes):
    smartest_superhero = [superheroes[0].name]
    if len(superheroes) > 1:
        for i in range(1, len(superheroes)):
            if superheroes[0].intelligence == superheroes[i].intelligence:
                smartest_superhero.append(superheroes[i].name)
    return ', '.join(smartest_superhero)


if __name__ == '__main__':

    superheroes_by_intelligence = get_superhero_intelligence_powerstats(
        ['Captain', 'Hullk', 'Big', 'Deadpool', 'Wonder', 'Thanos', 'Iron'])
    print(f"\nСамый умный супергерой: {get_smartest_superhero(superheroes_by_intelligence)}")
    print("ТОП умных супергероев:")
    for index, superhero in enumerate(superheroes_by_intelligence, 1):
        print(f"{index}.{superhero.name}, ум: {superhero.intelligence}")
