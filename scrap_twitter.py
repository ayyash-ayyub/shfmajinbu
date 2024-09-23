import pandas as pd
twitter_auth_token = '149d730626b18463799cd35c026c857751b9a9e2'

# ketik bash install_node.sh untuk nginstall node.js dependencies

# cari berdasarkan username
# username = 'DailyDarkWeb'
# search_keyword = f'from:{username} cyber security since:2024-04-01 until:2024-09-09 lang:en'
# limit = 100
# npx -y tweet-harvest@2.6.1 -o "{filename}" -s "{search_keyword}" --tab "LATEST" -l {limit} --token {twitter_auth_token} # type: ignore


# cari berdasarkan keyword
filename = 'result.csv'
search_keyword = 'cyber security since:2024-04-01 until:2024-09-09 lang:en'
limit = 100
npx -y tweet-harvest@2.6.1 -o "{filename}" -s "{search_keyword}" --tab "LATEST" -l {limit} --token {twitter_auth_token} # type: ignore

data ='result.csv'
result = pd.read_csv(data)

result.to_excel('hasil.xlsx', index=False)

