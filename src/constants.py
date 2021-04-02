IPL_MATCH_LIST_URL = 'https://www.espncricinfo.com/ipl2009/engine/match/index/series.html?search=ipl;series='
OVER_BY_OVER_URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/match/comments?seriesId={}&matchId={}&inningNumber={}&commentType=ALL&fromInningOver={}'
MATCH_DETAILS_URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/match/scorecard?seriesId={}&matchId={}'
PLAYER_STATS_URL = 'https://www.espncricinfo.com/india/content/player/{}.html'
LOG_SUMMARY_SHEET_ID = 1519789770
STATS_HEADER_LIST = [
    ['matches', 'bat_innings', 'not_outs', 'bat_runs', 'highest_score', 'bat_average', 'ball_faced', 'bat_strike_rate', '100', '50', '4s', '6s', 'catches', 'stumpings'],
    ['matches', 'bowl_innings', 'balls', 'bowl_runs', 'wickets', 'BBI', 'BBM', 'bowl_average', 'economy', 'bowl_strike_rate', '4w', '5w', '10']]
SCORECARD_FIELD_MAPPINGS = [{'is_batted': 'isBatted'}, {'runs': 'runs'}, {'balls': 'balls'}, {'fours': 'fours'}]
SCORECARD_FIELD_MAPPINGSS = [['is_batted','isBatted'], ['runs','runs'], ['balls','balls'], ['fours','fours'],
                            ['sixes','sixes'], ['is_out','isOut'], ['player_id','player||id'], ['fours','fours']
                             ]
