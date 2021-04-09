IPL_MATCH_LIST_URL = 'https://www.espncricinfo.com/ipl2009/engine/match/index/series.html?search=ipl;series='
OVER_BY_OVER_URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/match/comments?seriesId={}&matchId={}&inningNumber={}&commentType=ALL&fromInningOver={}'
MATCH_DETAILS_URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/match/scorecard?seriesId={}&matchId={}'
PLAYER_STATS_URL = 'https://www.espncricinfo.com/india/content/player/{}.html'
SERIES_DATA_URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/series/schedule?seriesId={}&fixtures=false'
PLAYER_DETAILS_URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/player/home?playerId={}'

STATS_HEADER_LIST = [['matches', 'bowl_innings', 'balls', 'bowl_runs', 'wickets', 'BBI', 'BBM', 'bowl_average', 'economy', 'bowl_strike_rate', 'fwk', 'fw', 'tw'],
                     ['matches', 'bat_innings', 'not_outs', 'bat_runs', 'highest_score', 'bat_average', 'ball_faced', 'bat_strike_rate', 'hundreds', 'fifties', 'fours', 'sixes',
                      'catches', 'stumpings']]
SCORECARD_FIELD_MAPPINGS = [{'is_batted': 'isBatted'}, {'runs': 'runs'}, {'balls': 'balls'}, {'fours': 'fours'}]
SCORECARD_FIELD_MAPPINGSS = [['batted_type', 'battedType'], ['runs', 'runs'], ['balls', 'balls'], ['fours', 'fours'],
                             ['sixes', 'sixes'], ['is_out', 'isOut'], ['player', 'player||id'], ['player_role_type', 'playerRoleType'],
                             ['dismissal_type', 'dismissalType'], ['dismissal_bowler', 'dismissalBowler||id'], ['dismissal_bowler_name', 'dismissalBowler||name'],
                             ['dismissal_text', 'dismissalText||long'],
                             ['fow_order', 'fowOrder'], ['fow_wicket_num', 'fowWicketNum'], ['fow_runs', 'fowRuns'], ['fow_overs', 'fowOvers']
                             ]
SCORECARD_BOWLING_FIELD_MAPPINGS = [['player', 'player||id'], ['overs', 'overs'], ['conceded', 'conceded'],
                                    ['wickets', 'wickets'], ['economy', 'economy'], ['dots', 'dots'],
                                    ['b_fours', 'fours'], ['b_sixes', 'sixes'], ['wides', 'wides'],
                                    ['noballs', 'noballs']]

INNINGS_FIELD_MAPPINGS = [['team', 'team||id'], ['innings_id', 'inningNumber'], ['is_batted', 'isBatted'],
                          ['runs', 'runs'], ['wickets', 'wickets'], ['lead', 'lead'],
                          ['target', 'target'], ['overs', 'overs'], ['total_overs', 'totalOvers'],
                          ['extras', 'extras'], ['byes', 'byes'], ['leg_byes', 'legbyes'], ['wides', 'wides'],
                          ['no_balls', 'noballs'], ['penalties', 'penalties']]

MATCH_FIELD_MAPPINGS = [['id', 'objectId'], ['date_of_match', 'startDate'], ['ground', 'ground||id'],
                        ['toss_winner', 'tossWinnerTeamId'], ['toss_decision', 'tossWinnerChoice'], ['winner', 'winnerTeamId'],
                        ['win_type', 'resultStatus'], ['series_object_id', 'series||objectId'], ['series', 'series||id'],
                        ['played_year', 'series||season']]

BALL_FIELD_MAPPINGS = [['inning_id', 'inningNumber'], ['ball_number', 'oversActual'], ['total_ball_runs', 'totalRuns'],
                       ['batsman_runs', 'batsmanRuns'], ['is_four', 'isFour'], ['is_six', 'isSix'],
                       ['is_wicket', 'isWicket'], ['byes', 'byes'], ['leg_byes', 'legbyes'],
                       ['wides', 'wides'], ['no_balls', 'noballs'], ['batsman', 'batsmanPlayerId'], ['bowler', 'bowlerPlayerId'],
                       ['total_runs', 'totalInningRuns'], ['title', 'title'], ['comment', 'commentTextItems||*html'], ['dismissal_type', 'dismissalType']
    , ['dismissal_text_short', 'dismissalText||short'], ['dismissal_text_long', 'dismissalText||long'], ['dismissal_text_commentary', 'dismissalText||commentary']]

ELASTIC_INDEX_LIST = ['player', 'statistics', 'team', 'ground', 'match_batting', 'match_bowling', 'matches', 'innings', 'ball_by_ball']
STATS_HEADER = {
    'BOWLING': [['matches', 'mt'], ['bowl_innings', 'in'], ['balls', 'bl'], ['bowl_runs', 'rn'], ['wickets', 'wk'], ['BBI', 'bbi'], ['BBM', 'bbm'], ['bowl_average', 'avg'],
                ['economy', 'bwe'], ['bowl_strike_rate', 'sr'], ['fwk', 'fwk'], ['fw', 'fw'], ['tw', 'tw']],
    'BATTING': [['matches', 'mt'], ['bat_innings', 'in'], ['not_outs', 'no'], ['bat_runs', 'rn'], ['highest_score', 'hs'], ['bat_average', 'avg'], ['ball_faced', 'bl'],
                ['bat_strike_rate', 'sr'], ['hundreds', 'hn'], ['fifties', 'ft'], ['fours', 'fo', ], ['sixes', 'si'], ['catches', 'ct'], ['stumpings', 'st']]}
