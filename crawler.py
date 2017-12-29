from github import Github
from pymongo import MongoClient
import os
import pickle
import json
import time

def crawl_user_info(user):
    """
    get user info
    :param user: class:`github.NamedUser.NamedUser`
    :return: user info. type of dict
    """
    info = {}
    info['name'] = user.name
    info['email'] = user.email
    info['location'] = user.location
    info['company'] = user.company
    info['num_followers'] = user.followers
    info['num_following'] = user.following
    info['contribution'] = user.contributions
    info['blog'] = user.blog
    info['url'] = user.html_url
    num_starred = 0
    starred_repos = []
    starreds = user.get_starred()
    for starred in starreds:
        starred_repos.append(starred.name)
        num_starred += 1
    info['num_starred'] = num_starred
    info['starred_repos'] = starred_repos
    repos = []
    REPOS = user.get_repos()
    for repo in REPOS:
        repos.append(repo.name)
    info['repos'] = repos
    return info

def update_to_be_crawl_users(user):
    """
    update to_be_crawl_users
    :param user: class:`github.NamedUser.NamedUser`
    :return: None, update inplace
    """
    followers = user.get_followers()
    followings = user.get_following()
    # duplication
    for follower in followers:
        if follower.login not in to_be_crawl_users and follower.login not in crawled_users:
            to_be_crawl_users.add(follower.login)
    for following in followings:
        if following.login not in to_be_crawl_users and following.login not in crawled_users:
            to_be_crawl_users.add(following.login)

def update_crawled_users(user_login):
    """update crawled users"""
    crawled_users.add(user_login)

def save_to_be_crawl_users():
    with open('to_be_crawl_users.pkl','wb') as f:
        pickle.dump(to_be_crawl_users, f)

def save_crawled_users():
    with open('crawled_users.pkl','wb') as f:
        pickle.dump(crawled_users, f)

def load_to_be_crawl_users():
    with open('to_be_crawl_users.pkl','rb') as f:
        to_be_crawl_users = pickle.load(f)
    return to_be_crawl_users

def load_crawled_users():
    with open('crawled_users.pkl','rb') as f:
        crawled_users = pickle.load(f)
    return crawled_users

def get_users(to_be_crawl_users):
    """
    popleft from to_be_crawl_users
    :param to_be_crawl_users: type of set, each element is user login
    :return: user login, type of string
    """
    user = to_be_crawl_users.pop()
    return user


if __name__ == '__main__':
    # setting MongoClient, db and collections
    client_mongo = MongoClient("10.18.125.17", 27017)
    db = client_mongo.github_data
    table = db.userinfo2
    # set time
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday
    # open json file
    file_name = 'user'+str(month)+str(day)
    file = open('user_info/' + file_name + '.json', 'a')
    # Specify your own access token here
    ACCESS_TOKEN = 'b24f994022fa215896e2748e1a7fd145bdcbe6e9 '
    client = Github(ACCESS_TOKEN)
    # define start user
    start_user_login = 'Johnson0722'
    # type of class(`github.NamedUser.NamedUser`)
    start_user = client.get_user(start_user_login)
    # define to_be_crawl_users, type of set. store user name
    if os.path.exists('to_be_crawl_users.pkl'):
        to_be_crawl_users = load_to_be_crawl_users()
        if len(to_be_crawl_users) == 0:
            to_be_crawl_users.add(start_user.login)
    else:
        to_be_crawl_users = set()
        to_be_crawl_users.add(start_user.login)
    # define crawled_users, type of set. store user name
    if os.path.exists('crawled_users.pkl'):
        crawled_users = load_crawled_users()
    else:
        crawled_users = set()

    while len(to_be_crawl_users) > 0:
        # get user instance
        try:
            user_login = get_users(to_be_crawl_users)
            user = client.get_user(user_login)
            info = crawl_user_info(user)
            # save to json file
            content = json.dumps(info, ensure_ascii=False) + '\n'
            file.write(content)
            # save data to mongo and json files
            table.insert_one(info)
            # update to_be_crawl_users and crawled_users
            update_crawled_users(user_login)
            if len(to_be_crawl_users) < 100:
                update_to_be_crawl_users(user)
        except:
            save_to_be_crawl_users()
            save_crawled_users()
            continue

