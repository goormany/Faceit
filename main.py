import requests
import datetime
import json
from rich.console import Console
from config import *
import csv
import os

console = Console()
data_base = []
pos = input('What position did you play? ')

headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0'
}

def get_data():
    url = f'https://api.faceit.com/stats/v1/stats/time/users/5476e8ef-c54a-4e05-9d56-6d65e3d27f3d/games/csgo?page=0&size={NUM_GAMES}'
    r = requests.get(url=url, headers=headers)

    # with open('r.json', 'w') as f:
    #     json.dump(r.json(), f, indent=4, ensure_ascii=False)

    data = r.json()
    data_list = []
    win_or_lose = 'None'
    items = data

    for item in items:
        date = item['date']
        matchId = item['matchId']
        map_csgo = item['i1']
        region = item['i0']
        score = item['i18']
        sum_rounds = item['i12']
        bestsof = item['bestOf']
        elo = item['elo']

        normal_date = datetime.datetime.fromtimestamp(date/1000)
        normal_date.isoformat()
            
        score = score.split(' / ')
        if score[0] > score[1]:
            win_or_lose = 'Victory'
            
        else:
            win_or_lose = 'Defeat'
            score = f'{score[0]} / {score[1]}'



        data_list.append(
            {
                'date': normal_date,
                'map': map_csgo,
                'Match outcome': win_or_lose,
                'region': region,
                'score': score,
                'sum_rounds': sum_rounds,
                'BO': bestsof,
                'new elo': elo,
                'roomID': matchId,
            }
        )

    url = f'https://api.faceit.com/stats/v1/stats/matches/{matchId}'
    r = requests.get(url=url, headers=headers)

    data = r.json()
    # items = data[0]['teams'][0]['players'][0]

    # with open('data.json', 'w') as f:
    #     json.dump(items, f, indent=4, ensure_ascii=False)
    my_stack = 0
    items = data[0]
    for item in items['teams'][0]['players']:
        nickname = item['nickname'],

        if nickname[0] in TEAMATES:
            my_stack += 1

        for player in nickname:
            if player == 'BLVCK7':
                kill = item['i6'],
                assists = item['i7'],
                death = item['i8'],
                kr = item['c3'],
                kd = item['c2'],
                hs = item['i13'],
                hsp = item['c4'],
                kda = f'{kill[0]}/{death[0]}/{assists[0]}'

                data_list.append(
                    {
                    'nickname': nickname,
                    'kill': kill,
                    'assists': assists,
                    'death': death,
                    'k/r': kr,
                    'k/d': kd,
                    'k/d/a': kda,
                    'hs count': hs,
                    'hs %': hsp,
                    'position': pos,
                    }
                )
            else:
                pass


    for item in items['teams'][1]['players']:
        nickname = item['nickname'],

        if nickname[0] in TEAMATES:
            my_stack += 1
        for player in nickname:
            if player == 'BLVCK7':
                kill = item['i6'],
                assists = item['i7'],
                death = item['i8'],
                kr = item['c3'],
                kd = item['c2'],
                hs = item['i13'],
                hsp = item['c4'],
                kda = f'{kill[0]}/{death[0]}/{assists[0]}'

                data_list.append(
                    {
                    'nickname': nickname,
                    'kill': kill,
                    'assists': assists,
                    'death': death,
                    'k/r': kr[0],
                    'k/d': kd,
                    'k/d/a': kda,
                    'hs count': hs,
                    'hs %': hsp[0],
                    'position': pos,
                    }
                )
            else:
                pass
    
    data_list.append(
        {
            'friends count': my_stack
        }
    )

    data_base.append(
        {
            'date': normal_date,
            'map': map_csgo,
            'new elo': elo,
            'k/d': kd,
            'k/d/a': kda,
            'hs %': hsp,
            'position': pos,
            'friends count': my_stack,
        }
    )
        


    console.print(f'[bold blue][INFO][/] [bold green]SUCCESS!!![/] [bold blue][INFO][/]')
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y-%H:%M")

    if os.path.exists('log/'):
        os.path.isdir('log/')
    else:
        os.mkdir('log/')
    with open(f'log/data_{cur_time}.json', 'a') as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False, default=str)
    with open('log/data.json', 'w') as f:
        json.dump(data_base, f, indent=4, ensure_ascii=False, default=str)
    
    if os.path.exists('data.csv'):
        pass

    else:
        with open('data.csv', 'w') as f: #, encoding='cp1251'
            writer = csv.writer(f)
            writer.writerow(
                ('Дата', 'карта', 'исход матча', 'счет', 'нью эло', 'кд', 'кда', 'хс%', 'позиция', 'фриендс каунт')
            )
    
    with open('data.csv', 'a') as f: #, encoding='cp1251'
            writer = csv.writer(f)
            writer.writerow(
                [normal_date, map_csgo, win_or_lose, score, elo, kd[0], kda, hsp[0], pos, my_stack]
            )



def main():
    get_data()


if __name__ == '__main__':
      main()