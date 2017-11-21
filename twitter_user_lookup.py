import tweepy
from tweepy import API


def get_twitter_users(api: API, user_ids: list) -> tweepy.models.ResultSet:
    users = api.lookup_users(user_ids=user_ids)
    return users
