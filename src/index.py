from src import constants
import requests
import json
from src import utils
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from elasticsearch import Elasticsearch


def find_series_and_match_id(external_series_id):
    match_ids = []
    return_obj = {
        'series_id': 0,
        'match_ids': match_ids
    }

    soup = utils.get_page_data_from_url(constants.IPL_MATCH_LIST_URL + external_series_id)
    matches = soup.findAll("div", attrs={"class": "match-articles"})

    number_of_matches = matches.__len__()
    first_match_url = matches[0].find("a").attrs.get('href')
    get_original_url = requests.get(first_match_url)
    parsed_url = urlparse(get_original_url.url)
    split_url = parsed_url.path.split("/")
    series_id = get_last_item(split_url[2])
    match_id = int(get_last_item(split_url[3]))

    for i in range(number_of_matches):
        match_ids.append(str(match_id + i))
    return_obj['series_id'] = series_id

    return return_obj


def get_last_item(input_param):
    split_input_block = input_param.split("-")
    return split_input_block[split_input_block.__len__() - 1]


def get_over_data(input_url):
    over_by_over_data = requests.get(input_url)
    export_data = []
    if over_by_over_data.status_code == 200:

        over_by_over_data_json = over_by_over_data.json()
        for ball in reversed(over_by_over_data_json.get('comments')):
            print(ball)
            comment = ""
            if ball.get('commentTextItems') is not None:
                comment = ball.get('commentTextItems')[0].get('html')
            play_side_info = get_played_area(comment)
            export_data.append(
                [ball.get('oversActual'), ball.get('overNumber'), ball.get('ballNumber'), comment, play_side_info.get('played_side'), play_side_info.get('off_or_leg')])
            print([ball.get('oversActual'), ball.get('overNumber'), ball.get('ballNumber'), comment, play_side_info.get('played_side'), play_side_info.get('off_or_leg')])


def get_played_area(comment):
    played_side = ""
    off_or_leg = ""
    off_sides = ["point", "gully", "slip", "cover", "long off", "mid off", "long-off", "mid-off", "third man", "third-man"]
    on_sides = ["fine leg", "short leg", "square leg", "mid wicket", "mid on", "long on", "fine-leg", "short-leg", "square-leg", "mid-wicket", "mid-on", "long-on", "midwicket"]

    for item in off_sides:
        if item in comment.lower():
            played_side = item.replace("-", "").replace(" ", "")
            off_or_leg = "Off"
    for item in on_sides:
        if item in comment.lower():
            played_side = item.replace("-", "").replace(" ", "")
            off_or_leg = "On"

    return {
        'played_side': played_side,
        'off_or_leg': off_or_leg
    }


def get_match_data(input_url):
    match_data = requests.get(input_url)
    if match_data.status_code == 200:
        print(match_data.json())
        es.index(index='matches', doc_type='doc', body=match_data.json())


def get_player_data(series_id, match_id):
    match_detail_url = constants.MATCH_DETAILS_URL.format(series_id, match_id)
    match_data = requests.get(match_detail_url)
    if match_data.status_code == 200:
        print(match_data.json().get("match").get("title"))
        # get_scorecard_data(match_id, match_data.json())
        ground_data_json = match_data.json().get("match").get("ground")
        ground_data = {
            'id': ground_data_json.get('id'),
            'longName': ground_data_json.get('longName'),
            'town': ground_data_json.get('town').get("name"),
            'country': ground_data_json.get('country').get("name")
        }
        if ground_data not in grounds_data:
            grounds_data.append(ground_data)
            es.update(index='grounds', doc_type='doc', id=ground_data.get('id'), body={'doc': ground_data, 'doc_as_upsert': True})

        team_data = match_data.json().get("content").get("matchPlayers").get("teamPlayers")
        for team in team_data:
            team_data_json = team.get("team")
            team_data = {
                'id': team_data_json.get("id"),
                'name': team_data_json.get("slug")
            }

            if team_data not in teams_data:
                teams_data.append(team_data)
                es.update(index='teams', doc_type='doc', id=team_data.get('id'), body={'doc': team_data, 'doc_as_upsert': True})

            player_data_array = team.get("players")
            for player in player_data_array:
                player_data_json = player.get('player')
                player_data = {
                    'id': player_data_json.get('id'),
                    'objectId': player_data_json.get('objectId'),
                    'name': player_data_json.get('name'),
                    'longName': player_data_json.get('longName'),
                    'battingName': player_data_json.get('battingName'),
                    'playingRole': player_data_json.get('playingRole'),
                    'longBattingStyle': player_data_json.get('longBattingStyle'),
                    'longBowlingStyle': player_data_json.get('longBowlingStyle')
                }
                if player_data not in players_data:
                    players_data.append(player_data)
                    player_stats = get_player_stats(player_data.get('objectId'))
                    es.update(index='statistics', doc_type='doc', id=player_stats.get('objectId'), body={'doc': player_stats, 'doc_as_upsert': True})
                    es.update(index='players', doc_type='doc', id=player_data.get('id'), body={'doc': player_data, 'doc_as_upsert': True})


def get_player_stats(object_id):
    return_object = {'objectId': object_id}
    player_id = object_id
    player_stats_html = utils.get_page_data_from_url(constants.PLAYER_STATS_URL.format(str(player_id)))
    for j in range(2):
        stats_table_contents = player_stats_html.findAll("tbody")[j].contents
        for i in range(len(stats_table_contents)):
            if i % 2 is 1:
                # print(stats_table_contents[i].findAll("td")[0].contents[0].contents[0].lower())
                if stats_table_contents[i].findAll("td")[0].contents[0].contents[0].lower() in 't20s':
                    count = 0
                    for row_data in stats_table_contents[i].findAll("td")[1:]:
                        return_object.update({constants.STATS_HEADER_LIST[j][count]: str(row_data.contents[0])})
                        count = count + 1
    return return_object


def get_scorecard_data(match_id, match_data_json):
    scorecard_object = {
        "match_id": match_id,
    }
    for inning in match_data_json.get("content").get("scorecard").get("innings"):
        scorecard_object.update({'innings_id': inning.get("inningNumber")})
        batting_data = inning.get("inningBatsmen")
        for batsman in batting_data:
            for entry in constants.SCORECARD_FIELD_MAPPINGSS:
                scorecard_object.update({entry[0]: batsman.get(entry[1])})
    print("ggg")


# player_stats_html.findAll("tbody")[0].contents[11].findAll("td")[0].contents[0].contents[0]
# how to have multiple entries
# years team attended the season
# get latest player data jj hh

if __name__ == '__main__':
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    teams_data = []
    players_data = []
    grounds_data = []
    series_and_match_ids = find_series_and_match_id("4801")
    inning = 1
    over = 4
    for match in series_and_match_ids.get('match_ids'):
        get_player_data(series_and_match_ids.get('series_id'), match)
    # get_match_data(match_detail_url)
    # for j in range(1, 3):
    #    for i in range(2, 24, 2):
    #        match_over_by_over_url = constants.OVER_BY_OVER_URL.format(series_and_match_ids.get('series_id'), series_and_match_ids.get('match_ids')[0], j, i)
    #        get_over_data(match_over_by_over_url)
    print("Exit")
