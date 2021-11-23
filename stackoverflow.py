import json
from datetime import datetime

import requests

# Today date in seconds since the 1st January 1970 (Unix time)
TODAY_DATE_IN_SECONDS = datetime.today().timestamp()


def _get_parameters(page, tag, last_n_days):
    return {
        'page': page,
        'pagesize': 100,
        'order': 'desc',
        'sort': 'creation',
        'site': 'stackoverflow',
        'tagged': tag,
        'fromdate': round(TODAY_DATE_IN_SECONDS - 86400 * last_n_days),
        'todate': round(TODAY_DATE_IN_SECONDS)
    }


def get_last_questions_on_stackoverflow(tag, last_n_days):
    next_page = 1
    has_more = True
    questions = []

    while has_more:
        print(f'Fetching page {next_page} ...')
        parameters = _get_parameters(next_page, tag, last_n_days)
        response = requests.get(url='https://api.stackexchange.com/2.3/questions', params=parameters)
        response.raise_for_status()

        if response.status_code == 200:
            for item in response.json().get('items'):
                question = item.get('title')
                question_link = item.get('link')
                questions.append(dict(question=question, link=question_link))
            next_page += 1
            has_more = response.json().get('has_more')
        else:
            print('Error!')
            has_more = False

    return questions


if __name__ == '__main__':
    data = get_last_questions_on_stackoverflow(tag='Python', last_n_days=2)
    with open('stackoverflow_python_questions.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    # pprint(data)
