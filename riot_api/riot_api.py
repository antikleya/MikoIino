import requests

valid_regions = {'EUW': 'euw1', 'RU': 'ru'}


class ReturnedValue:
    valid = bool
    text = str

    def __init__(self, valid: bool, text: str):
        self.valid = valid
        self.text = text


def get_time_shift(tier: str):
    if tier == '4':
        return 0
    if tier == '3':
        return 145 * 60
    if tier == '2':
        return 180 * 60
    if tier == '1':
        return 210 * 60


def get_summoner_id(region: str, summoner_name: str, key: str):
    url = 'https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + key
    response = requests.get(url)
    if response.status_code != 200:
        return ReturnedValue(False, 'Something went wrong with summoner name api request, status code = ' + str(
            response.status_code))
    summoner_id = response.json()['id']
    return ReturnedValue(True, str(summoner_id))


def get_team_id(region: str, summoner_id: str, key: str):
    url = 'https://' + region + '.api.riotgames.com/lol/clash/v1/players/by-summoner/' + summoner_id + '?api_key=' + key
    response = requests.get(url)
    if response.status_code != 200:
        return ReturnedValue(False, 'Something went wrong with team id api request, status code = ' + str(
            response.status_code))
    team_id = response.json()[0]['teamId']
    return ReturnedValue(True, str(team_id))


def get_tier(region: str, team_id: str, key: str):
    url = 'https://' + region + '.api.riotgames.com/lol/clash/v1/teams/' + team_id + '?api_key=' + key
    response = requests.get(url)
    if response.status_code != 200:
        return ReturnedValue(False, 'Something went wrong with team tier api request, status code = ' + str(
            response.status_code))
    team_tier = response.json()['tier']
    return ReturnedValue(True, str(team_tier))


def get_tournament_schedule(request: list, key: str):
    if len(request) < 4:
        return ReturnedValue(False, 'Not a valid request')

    region = request[3]
    if region.upper() not in valid_regions.keys():
        return ReturnedValue(False, 'Not a valid region')

    url = 'https://' + valid_regions[region.upper()] + '.api.riotgames.com/lol/clash/v1/tournaments?api_key=' + key
    _response = requests.get(url)
    if _response.status_code != 200:
        return ReturnedValue(False, 'Something went wrong with tournament api request, status code = ' + str(_response.status_code))

    response_json = _response.json()
    schedule = list()
    for i in response_json:
        schedule.append(str(i['schedule'][0]['registrationTime']))
    schedule = ' '.join(schedule)
    return ReturnedValue(True, schedule)


def get_clash_time(request: list, key: str):
    uncorrected_schedule = get_tournament_schedule(request, key)
    if not uncorrected_schedule.valid:
        return uncorrected_schedule

    uncorrected_schedule = list(map(int, uncorrected_schedule.text.split()))
    region = valid_regions[request[3].upper()]
    summoner_name = request[4]
    summoner_id = get_summoner_id(region, summoner_name, key)
    if not summoner_id.valid:
        return summoner_id
    team_id = get_team_id(region, summoner_id.text, key)
    if not team_id.valid:
        return team_id
    tier = get_tier(region, team_id.text, key)
    if not tier.valid:
        return tier
    shift = get_time_shift(tier.text)
    for i in range(len(uncorrected_schedule)):
        uncorrected_schedule[i] = str(uncorrected_schedule[i] + shift)
    corrected_schedule = ' '.join(uncorrected_schedule)
    return ReturnedValue(True, corrected_schedule)
