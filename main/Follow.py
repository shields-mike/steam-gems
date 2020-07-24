import Gems
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
                count=10,
                since_id=f"{self.id_num}",
            )

            id_file.seek(0)
            id_file.write(str(self.tweets[0].id))

    def get_users(self):
        self.user_list = set()

        with open("follower_list", "r+") as file:
            for tweet in self.tweets:
                file.seek(0)
                content = file.read()

                if tweet.user.screen_name not in content:
                    self.user_list.add(tweet.user.screen_name)
                    file.write(tweet.user.screen_name + "\n")

    def follow_user(self):
        for acc in self.user_list:
            self.api.create_friendship(acc)


def main():
    api = Gems.authorize_twitter()

    twitter_bot = Follow4Follow(api)

    twitter_bot.get_tweets()
    twitter_bot.get_users()
    twitter_bot.follow_user()


if __name__ == "__main__":
    main()

