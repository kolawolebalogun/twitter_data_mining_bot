import traceback

import re
from tweepy.streaming import StreamListener
import json

from google_sheet_sync import insert_row
from twitter_user_lookup import get_twitter_users


class TimelineListener(StreamListener):
    def __init__(self, api, tags):
        super().__init__(api)
        self.api = api
        self.tags = tags

    def on_data(self, data):
        try:
            data = json.loads(data)
            user = data.get("user")
            entities = data.get('entities')

            if user and entities:
                profile_name = user.get('screen_name')
                number_of_followers = user.get('followers_count')
                user_description = user.get('description')
                hashtags = [x.get('text').lower() for x in entities.get('hashtags')]

                # Check if specified tag in stream hash tag to refine result to more useful ones
                detected_tags = [x for x in self.tags if x.lower().replace("#", "") in hashtags]
                if detected_tags:
                    print(" "
                          "[x] Profile name: ", profile_name, '\n',
                          "[x] Number of followers: ", number_of_followers, '\n',
                          "[x] User description: ", user_description, '\n',
                          "[x] Hash Tags:", hashtags)

                    # Uncomment next line if you want to see the expanded details of user
                    # user_expanded_details = get_twitter_users(self.api, [user.get('id')])

                    # Check if user account is public/open
                    if not user.get('protected'):
                        # Check if user has between 1,000-50,000 followers
                        if 1000 <= number_of_followers <= 50000:
                            # Write to google sheet
                            # Check for emails in user description
                            find_email = get_email_for_string(user_description)
                            email = ", ".join(
                                get_email_for_string(user_description)) if find_email else profile_name
                            google_sheet_values = [email, profile_name, number_of_followers, ", ".join(self.tags)]
                            insert_row(google_sheet_values)
        except:
            traceback.print_exc()

        print("-" * 500)
        return True

    def on_error(self, status):
        print(status)


def get_email_for_string(value):
    return re.findall(r'([a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)', value, re.M | re.I)
