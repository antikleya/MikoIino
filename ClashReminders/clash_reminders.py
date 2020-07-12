import requests
import time
from multiprocessing import Process

region_consts = {'EUW': 'euw1', 'RU': 'ru', 'euw1': 'euw1', 'ru': 'ru'}
supported_regions = ['euw1', 'ru']
# for now api_key filename is implemented as a constant
path_to_api = 'key'


class GeneralReminder:
    _api_key = str
    _region = str
    _team_name = str
    processes = []

    def get_region(self):
        return _region

    def send_reminder(self, message: str):
        # to do: implement the reminding
        print(message)
        pass

    def get_tournament_schedule(self):
        url = url = 'https://' + self._region + '.api.riotgames.com/lol/clash/v1/tournaments?api_key=' + self._api_key
        response = requests.get(url)
        assert response.status_code == 200
        return response.json()


class TeamReminder(GeneralReminder):

    def __init__(self, filename: str, region: str):
        self._region = region_consts[region.upper()]
        self._api_key = open(filename, 'r').read()
        self._team_name = 'temp'

    def start_reminder(self, target_times: list):
        try:
            for i in target_times:
                tmp = time.time()
                assert i > tmp
                time.sleep(i - tmp)
                self.send_reminder('temp message')
        except AssertionError:
            print("cringe happened with reminder time")
            return

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
        process = Process(target=self.start_reminder, args=([reminder_time_day1, reminder_time_day2]))
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

    def start_reminder(self, target_time: int, additional_func):
        try:
            tmp = time.time()
            assert target_time > tmp
            time.sleep(target_time - tmp)
            self.send_reminder("temp message")
        except AssertionError:
            print('cringe happened with beginning of the week reminder time')
            return
        additional_func()

    def setup_reminder(self, func):
        response_json = self.get_tournament_schedule()
        tournament_time = time.localtime(response_json[0]['schedule'][0]['registrationTime'] // 1000)
        target_time = time.mktime(tournament_time) - (tournament_time.tm_wday-1)*24*60*60
        process = Process(target=self.start_reminder, args=(target_time, func))
        self.processes.append(process)
        process.start()


# to do
class ReminderService:
    _reminders = {}

    def __init__(self):
        for i in supported_regions:
            self._reminders[i] = {'team_reminders': [], 'week_start_reminder': BeginningOfTheWeekReminder(path_to_api, i)}

    def _update_reminder(self, obj):
        region = obj.get_region()
        time_obj = time.localtime(time.time())
        time_obj.tm_wday = 6
        time_obj.tm_hour = 13
        time_obj.tm_min = 0
        time_obj.tm_sec = 0
        target_time = time.mktime(time_obj)
        time.sleep(target_time - time.time())
        rem_list = self._reminders[obj.get_region()]['team_reminders']
        for i in rem_list:
            i.setup_reminder('sindol')  # to do: implement a method to get summoner names by team
        time.sleep(47*60*60)
        obj.setup_reminder(self._update_reminder)

    def add_team_reminder(self, region: str):
        assert region in supported_regions
        self._reminders[region]['team_reminders'].append(TeamReminder(path_to_api, region))


def garbage():
    print("garbage")


rem = BeginningOfTheWeekReminder('key', 'euw')
rem.start_reminder(time.time()+10, garbage)

