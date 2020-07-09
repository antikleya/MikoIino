import requests
import time
from multiprocessing import Process

region_consts = {'EUW': 'euw1', 'RU': 'ru'}
# for now api_key filename is implemented as a constant
path_to_api = 'key'


class GeneralReminder:
    _api_key = str
    _region = str
    _team_name = str
    processes = []

    def send_reminder(self, message: str):
        # to do: implement the reminding
        print(message)
        pass

    def get_tournament_schedule(self):
        url = url = 'https://' + self._region + '.api.riotgames.com/lol/clash/v1/tournaments?api_key=' + self._api_key
        response = requests.get(url)
        assert response.status_code == 200
        return response.json()

    def start_reminder(self, target_times: list, messages: list, additional_func):
        for i in range(len(target_times)):
            tmp = time.time()
            assert target_times[i] > tmp
            time.sleep(target_times[i] - tmp)
            self.send_reminder(messages[i])
        additional_func()


class TeamReminder(GeneralReminder):

    def __init__(self, filename: str, region: str):
        self._region = region_consts[region.upper()]
        self._api_key = open(filename, 'r').read()
        self._team_name = 'temp'

    def empty_reset_func(self):
        pass

    def _get_url(self, mode: str, param: str = ''):      # modes: summoner_by_name, team_by_summid, team_info
        url = 'https://' + self._region + '.api.riotgames.com/lol/'
        if mode == 'summoner_by_name':
            url += "summoner/v4/summoners/by-name/" + param
        if mode == 'team_by_summid':
            url += "clash/v1/players/by-summoner/" + param
        if mode == 'team_info':
            url += "clash/v1/teams/" + param
        url += "?api_key=" + self._api_key
        return url

    def _get_time_shift_by_tier(self, tier: int):
        if tier == 1:
            return 0
        if tier == 2:
            return 145*60
        if tier == 3:
            return 180*60
        if tier == 4:
            return 210*60

    def setup_reminder(self, summoner_name: str):
        reminder_time_day1, reminder_time_day2, self._team_name = self.clash_time_by_name(summoner_name)
        process = Process(target=self.start_reminder, args=([reminder_time_day1, reminder_time_day2],
                                                            ['cringe message 1', 'cringe message 2']))
        self.processes.append(process)
        process.start()

    def clash_time_by_name(self, name: str):
        try:
            # getting summoner id
            url = self._get_url('summoner_by_name', name)
            response = requests.get(url)
            assert response.status_code == 200
            summoner_id = response.json()['id']

            # getting team id
            url = self._get_url('team_by_summid', summoner_id)
            response = requests.get(url)
            assert response.status_code == 200
            team_id = response.json()[0]['teamId']

            # getting team tier and name
            url = self._get_url('team_info', team_id)
            response = requests.get(url)
            assert response.status_code == 200
            response_json = response.json()
            team_tier = response_json['tier']
            team_name = response_json['name']

            # getting tournament schedule
            response_json = self.get_tournament_schedule()
            first_schedule = response_json[0]['schedule'][0]['registrationTime']
            second_schedule = response_json[1]['schedule'][0]['registrationTime']

            # finalizing results
            first_schedule = first_schedule // 1000 + self._get_time_shift_by_tier(team_tier)
            second_schedule = second_schedule // 1000 + self._get_time_shift_by_tier(team_tier)
            return first_schedule, second_schedule, team_name

        except AssertionError:
            print('Api posted some cringe ( response status code != 200 ).')
            return -1, -1, 'b'


class BeginningOfTheWeekReminder(GeneralReminder):

    def __init__(self, filename: str, region: str):
        self._api_key = open(filename, 'r').read()
        self._region = region_consts[region.upper()]

    def empty_shit(self):
        pass

    def setup_reminder(self):
        response_json = self.get_tournament_schedule()
        tournament_time = time.localtime(response_json[0]['schedule'][0]['registrationTime'] // 1000)
        target_time = time.mktime(tournament_time) - (tournament_time.tm_wday-1)*24*60*60
        print(time.localtime(target_time))
        process = Process(target=self.start_reminder, args=([target_time], ['cringe message'], self.empty_shit))
        self.processes.append(process)
        process.start()


# to do
class ReminderService:
    reminders = []


# rem = BeginningOfTheWeekReminder('key', 'euw')
# rem.setup_reminder()
