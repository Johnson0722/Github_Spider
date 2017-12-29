import json
import pandas as pd
import numpy as np
import os

total_user_info = []

columns = ['name', 'email', 'location','company',
           'num_followers', 'num_following', 'url', 'blog',
           'num_starred', 'repos', 'starred_repos']

dir_ = 'user_info'

file = 'user1124'

file_name = os.path.join(dir_,file)

with open(file_name + '.json', encoding='utf-8') as f:
    for line in f:
        info = json.loads(line)
        user_info = [info['name'], info['email'], info['location'],  info['company'],
                     info['num_followers'], info['num_following'], info['url'],info['blog'],
                     info['num_starred'], info['repos'], info['starred_repos']]
        total_user_info.append(user_info)

user_df = pd.DataFrame(np.array(total_user_info), columns=columns)

user_df.to_csv(file_name + '.csv', index=False)


