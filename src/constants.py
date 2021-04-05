IPL_MATCH_LIST_URL = 'https://www.espncricinfo.com/ipl2009/engine/match/index/series.html?search=ipl;series='
OVER_BY_OVER_URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/match/comments?seriesId={}&matchId={}&inningNumber={}&commentType=ALL&fromInningOver={}'
MATCH_DETAILS_URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/match/scorecard?seriesId={}&matchId={}'
PLAYER_STATS_URL = 'https://www.espncricinfo.com/india/content/player/{}.html'
SERIES_DATA_URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/series/schedule?seriesId={}&fixtures=false'
LOG_SUMMARY_SHEET_ID = 1519789770
STATS_HEADER_LIST = [
    ['matches', 'bat_innings', 'not_outs', 'bat_runs', 'highest_score', 'bat_average', 'ball_faced', 'bat_strike_rate', '100', '50', '4s', '6s', 'catches', 'stumpings'],
    ['matches', 'bowl_innings', 'balls', 'bowl_runs', 'wickets', 'BBI', 'BBM', 'bowl_average', 'economy', 'bowl_strike_rate', '4w', '5w', '10']]
SCORECARD_FIELD_MAPPINGS = [{'is_batted': 'isBatted'}, {'runs': 'runs'}, {'balls': 'balls'}, {'fours': 'fours'}]
SCORECARD_FIELD_MAPPINGSS = [['batted_type', 'battedType'], ['runs', 'runs'], ['balls', 'balls'], ['fours', 'fours'],
                             ['sixes', 'sixes'], ['is_out', 'isOut'], ['player_id', 'player||id'], ['playerRoleType', 'playerRoleType'],
                             ['dismissal_type', 'dismissalType'], ['dismissal_bowler_id', 'dismissalBowler||id'], ['dismissal_bowler_name', 'dismissalBowler||name'],
                             ['dismissal_text', 'dismissalText||long'],
                             ['fow_order', 'fowOrder'], ['fow_wicket_num', 'fowWicketNum'], ['fow_runs', 'fowRuns'], ['fow_overs', 'fowOvers']
                             ]
SCORECARD_BOWLING_FIELD_MAPPINGS = [['player_id', 'player||id'], ['overs', 'overs'], ['conceded', 'conceded'],
                                    ['wickets', 'wickets'], ['economy', 'economy'], ['dots', 'dots'],
                                    ['b_fours', 'fours'], ['b_sixes', 'sixes'], ['wides', 'wides'],
                                    ['noballs', 'noballs']]

INNINGS_FIELD_MAPPINGS = [['team_id', 'team||id'], ['innings_id', 'inningNumber'], ['is_batted', 'isBatted'],
                          ['runs', 'runs'], ['wickets', 'wickets'], ['lead', 'lead'],
                          ['target', 'target'], ['overs', 'overs'], ['totalOvers', 'totalOvers'],
                          ['extras', 'extras'], ['byes', 'byes'], ['legbyes', 'legbyes'], ['wides', 'wides'],
                          ['noballs', 'noballs'], ['penalties', 'penalties']]

MATCH_FIELD_MAPPINGS = [['match_id', 'objectId'], ['date', 'startDate'], ['ground', 'ground||id'],
                        ['toss_winner_id', 'tossWinnerTeamId'], ['toss_decision_id', 'tossWinnerChoice'], ['winner_team_id', 'winnerTeamId'],
                        ['win_type', 'resultStatus'], ['series_object_id', 'series||objectId'], ['series_id', 'series||id'],
                        ['year', 'series||season']]

BALL_FIELD_MAPPINGS = [['inningNumber', 'inningNumber'], ['ball_number', 'oversActual'], ['total_ball_runs', 'totalRuns'],
                        ['batsman_runs', 'batsmanRuns'], ['is_four', 'isFour'], ['is_Six', 'isSix'],
                        ['is_wicket', 'isWicket'], ['byes', 'byes'], ['legbyes', 'legbyes'],
                        ['wides', 'wides'],['no_balls', 'noballs'], ['batsman_id', 'batsmanPlayerId'], ['bowler_id', 'bowlerPlayerId'],
                       ['total_runs', 'totalInningRuns'],['title', 'title'], ['comment', 'commentTextItems||*html'], ['dismissalType', 'dismissalType']
    ,['dismissal_text_short', 'dismissalText||short'], ['dismissal_text_long', 'dismissalText||long'], ['dismissal_text_commentary', 'dismissalText||commentary']]

ELASTIC_INDEX_LIST = ['players', 'statistics', 'teams', 'grounds', 'batting', 'bowling', 'match', 'innings', 'ball_by_ball']
