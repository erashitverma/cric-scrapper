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
    series_id = utils.get_last_item(split_url[2])
    match_id = int(utils.get_last_item(split_url[3]))

    for i in range(number_of_matches):
        match_ids.append(str(match_id + i))
    return_obj['series_id'] = series_id

    return return_obj


def get_new_series_match_id(series_id):
    match_ids = []
    return_obj = {
        'series_id': series_id,
        'match_ids': match_ids
    }
    series_detail_url = constants.SERIES_DATA_URL.format(series_id)
    series_data = requests.get(series_detail_url).json()
    for match in series_data.get('content').get('matches'):
        match_ids.append(match.get('objectId'))
    return return_obj


def get_over_data(input_url):
    over_by_over_data = requests.get(input_url)
    export_data = []
    if over_by_over_data.status_code == 200:
        over_by_over_data_json = over_by_over_data.json()
        for ball in reversed(over_by_over_data_json.get('comments')):
            # print(ball)
            comment = ""
            if ball.get('commentTextItems') is not None:
                comment = ball.get('commentTextItems')[0].get('html')
            play_side_info = get_played_area(comment)
            gg = utils.extract_json_from_source({}, [ball], constants.BALL_FIELD_MAPPINGS)
            gg[0].update(play_side_info)
            export_data.append(gg)
        for ball in export_data:
            utils.create_elastic_search_index(ball[0], "ball_by_ball", es)


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


def get_player_data(series_id, match_id):
    # match_id = 392238
    match_detail_url = constants.MATCH_DETAILS_URL.format(series_id, match_id)
    print(match_detail_url)
    match_data = requests.get(match_detail_url)
    if match_data.status_code == 200:
        print(match_data.json().get("match").get("title"))
        is_no_result = match_data.json().get("match").get("status")
        if is_no_result in "ABANDONED":
            get_match_basic_data(match_data.json(), False)
        else:
            get_match_basic_data(match_data.json(), True)
            get_scorecard_data(match_id, match_data.json())
            get_innings_data(match_id, match_data.json())
            ground_data_json = match_data.json().get("match").get("ground")
            ground_data = {
                'id': ground_data_json.get('id'),
                'long_name': ground_data_json.get('longName'),
                'town': ground_data_json.get('town').get("name"),
                'country': ground_data_json.get('country').get("name")
            }
            if ground_data not in grounds_data:
                grounds_data.append(ground_data)
                utils.update_elastic_search_index(ground_data, 'ground', es, ground_data.get('id'))

            team_data = match_data.json().get("content").get("matchPlayers").get("teamPlayers")
            for team in team_data:
                team_data_json = team.get("team")
                team_data = {
                    'id': team_data_json.get("id"),
                    'name': team_data_json.get("slug")
                }

                if team_data not in teams_data:
                    teams_data.append(team_data)
                    utils.update_elastic_search_index(team_data, 'team', es, team_data.get('id'))

                player_data_array = team.get("players")
                for player in player_data_array:
                    player_data_json = player.get('player')
                    player_data = {
                        'id': player_data_json.get('id'),
                        'object_id': player_data_json.get('objectId'),
                        'name': player_data_json.get('name'),
                        'long_name': player_data_json.get('longName'),
                        'batting_name': player_data_json.get('battingName'),
                        'playing_role': player_data_json.get('playingRole'),
                        'long_batting_style': player_data_json.get('longBattingStyle'),
                        'long_bowling_style': player_data_json.get('longBowlingStyle')
                    }
                    if player_data not in players_data:
                        players_data.append(player_data)
                        player_stats = get_player_stats_by_json(player_data.get('object_id'))
                        utils.update_elastic_search_index(player_stats, 'statistics', es, player_stats.get('object_id'))
                        utils.update_elastic_search_index(player_data, 'player', es, player_data.get('id'))


def get_player_stats_by_json(object_id):
    return_object = {'object_id': object_id}
    player_id = object_id
    players_data_json = requests.get(constants.PLAYER_DETAILS_URL.format(str(player_id))).json()
    for stats in players_data_json.get('content').get('careerAverages').get('stats'):
        if stats.get('cl') == 6:
            return_object.update(utils.extract_json_from_source(return_object, [stats], constants.STATS_HEADER.get(stats.get('type')))[0])
    return return_object


def get_scorecard_data(match_id, match_data_json):
    scorecard_object = {
        "match_id": match_id,
    }
    all_batting_data = []
    all_bowlings_data = []
    for inning in match_data_json.get("content").get("scorecard").get("innings"):
        scorecard_object.update({'innings_id': inning.get("inningNumber")})
        batting_data = inning.get("inningBatsmen")
        all_batting_data.append(
            utils.extract_json_from_source({"match_id": match_id, 'innings_id': inning.get("inningNumber")}, batting_data, constants.SCORECARD_FIELD_MAPPINGSS, True))
        bowling_data = inning.get("inningBowlers")
        all_bowlings_data.append(
            utils.extract_json_from_source({"match_id": match_id, 'innings_id': inning.get("inningNumber")}, bowling_data, constants.SCORECARD_BOWLING_FIELD_MAPPINGS))
    for inning_batsman in all_batting_data:
        for batsman in inning_batsman:
            utils.create_elastic_search_index(batsman, "match_batting", es)
    for innings_bowler in all_bowlings_data:
        for bowler in innings_bowler:
            utils.create_elastic_search_index(bowler, "match_bowling", es)


def get_innings_data(match_id, match_data_json):
    for inning in match_data_json.get("content").get("scorecard").get("innings"):
        utils.create_elastic_search_index(utils.extract_json_from_source({"match_id": match_id}, [inning], constants.INNINGS_FIELD_MAPPINGS)[0], "innings", es)


def get_match_basic_data(match_data_json, is_result):
    title = match_data_json.get("match").get("title")
    is_semi = "Semi-Final" in title
    is_final = "Final" == title
    match_details_json = utils.extract_json_from_source({}, [match_data_json.get("match")], constants.MATCH_FIELD_MAPPINGS)[0]
    match_details_json.update(
        {'match_order': match_counter + 1, 'title': title, 'is_semi': is_semi, 'is_final': is_final, 'team_one': match_data_json.get("match").get('teams')[0].get('id'),
         'team_two': match_data_json.get("match").get('teams')[1].get('id')})
    if is_result:
        match_details_json.update({'player_of_the_match': match_data_json.get('content').get('supportInfo').get('playersOfTheMatch')[0].get('player').get('id')})
    utils.create_elastic_search_index(match_details_json, "matches", es)


# player_stats_html.findAll("tbody")[0].contents[11].findAll("td")[0].contents[0].contents[0]
# how to have multiple entries
# years team attended the season
# get latest player data jj hh

if __name__ == '__main__':
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    utils.delete_all_elastic_index(es)
    teams_data = []
    players_data = []
    grounds_data = []
    match_counter = 0
    series_and_match_ids = get_new_series_match_id("466304")
    for match in reversed(series_and_match_ids.get('match_ids')):
        get_player_data(series_and_match_ids.get('series_id'), match)
        for j in range(1, 3):
            for i in range(2, 24, 2):
                match_over_by_over_url = constants.OVER_BY_OVER_URL.format(series_and_match_ids.get('series_id'), match, j, i)
                get_over_data(match_over_by_over_url)
    print("Exit")
