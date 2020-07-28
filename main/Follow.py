import os
import tweepy


class Follow4Follow:
    def __init__(self, api):
        self.api = api

    def get_tweets(self):
        with open("id.txt", "w+") as id_file:
            self.id_num = id_file.read()

            self.tweets = self.api.search(
                "#indiegame -filter:retweets",
                result_type="recent",
                count=20,
                since_id=f"{self.id_num}",
            )

            id_file.seek(0)
            id_file.write(str(self.tweets[0].id))

    def get_users(self):
        self.user_list = set()

        with open("follower_list.txt", "r+") as file:
            for tweet in self.tweets:
                file.seek(0)
                content = file.read()

                if tweet.user.screen_name not in content:
                    self.user_list.add(tweet.user.screen_name)
                    file.write(tweet.user.screen_name + "\n")

    def follow_user(self):
        for acc in self.user_list:
            self.api.create_friendship(acc)


def authorize_twitter():
    api_key = os.environ.get("twitter_api_key")
    api_secret = os.environ.get("twitter_api_key_secret")
    access_token = os.environ.get("twitter_access_token")
    access_secret = os.environ.get("twitter_access_token_secret")

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)

    return tweepy.API(auth)


def main():
    api = authorize_twitter()

    twitter_bot = Follow4Follow(api)

    twitter_bot.get_tweets()
    twitter_bot.get_users()
    twitter_bot.follow_user()


if __name__ == "__main__":
    main()

