import requests
import json
import pandas as pd

HOST = 'https://www.speedrun.com/api/v1/'
GAME_ID = '268zey6p' # id for majora's mask

def main():
    final_data = add_time()
    sorted = pd.Series(final_data).sort_values(ascending=False)
    final_data = sorted.apply(convert_to_hours)

    final_data.to_csv('speedrunners.csv')


def make_list():
    full_list = []
    offset = 0
    runs = requests.get(HOST + 'runs?max=200&game=' + GAME_ID).text
    dict = json.loads(runs)

    # loop through all pages (max 200 runs/page) and add to one big list
    while dict['pagination']['size'] == 200:
        runs = requests.get(HOST + '/runs?max=200&game=' + GAME_ID + '&offset=' + str(offset)).text
        dict = json.loads(runs)
        full_list.extend(dict['data'])
        offset += 200

        return full_list

def id_to_username(id):
    user_info = json.loads(requests.get(HOST + 'api/v1/users/' + id).text)

    if user_info.get('data'): # not sure why data key errors are happening here
        username = user_info['data']['names']['international']
    else:
        return 'fail'

    return username

def add_time():
    runs = make_list()
    player_times = {}
    id_names = {}
    final = {}
    ids = set()

    for i in range(len(runs)):
        if runs[i]['players'][0].get('id'):
            player = runs[i]['players'][0]['id']
            ids.add(player)
        else:
            player = runs[i]['players'][0]['name']


        time = runs[i]['times']['primary_t']

        if player in player_times:
            player_times[player] += time
        else:
            player_times[player] = time

    # create a mapping of ids to usernames
    for id in ids:
        id_names[id] = id_to_username(id)

    for id in id_names.keys() & player_times.keys():
        final[id_names[id]] = player_times[id]

    return final

def convert_to_hours(seconds):
  m, s = divmod(seconds, 60)
  h, m = divmod(m, 60)

  return str(int(h)) + ':' + str(int(m)) + ':' + str(int(s))

if __name__ == '__main__':
    #main()
    runs = requests.get(HOST + 'runs?max=200&game=' + GAME_ID).text
    dict = json.loads(runs)
    print (dict.keys())