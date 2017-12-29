from pymongo import MongoClient
import pandas as pd
import numpy as np

client = MongoClient("10.18.125.17", 27017)
db = client.github_data
table = db.userinfo2

total_user_info = []

columns = ['name', 'email', 'location','company',
           'num_followers', 'num_following', 'url', 'blog',
           'num_starred', 'repos', 'starred_repos']

for info in table.find():
    user_info = [info['name'], info['email'], info['location'],  info['company'],
                 info['num_followers'], info['num_following'], info['url'],info['blog'],
                 info['num_starred'], info['repos'], info['starred_repos']]
    total_user_info.append(user_info)


user_df = pd.DataFrame(np.array(total_user_info), columns=columns)

user_df.to_csv('user_1123.csv', index=False)
