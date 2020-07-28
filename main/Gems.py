import requests
import bs4
import datetime
import pickle
import random
import os
import tweepy
import shutil


class Website:
    def __init__(self, game_block):
        self.game_block = game_block

    def game(self):
        self.game_name = self.game_block.find("span", class_="title")

    def link(self):
        link_block = self.game_block.find("span", class_="title")
        self.link_250 = link_block.find("a")["href"]

    def steam(self):
        self.steam_link = self.game_block.find("a", class_="store")["href"]

    def ranking(self):
        game_num = self.link_250.split("/")[4].strip()
        self.rank = f"https://steam250.com/hidden_gems#app/{game_num}"


class File(Website):
    def __init__(self, game_block, txt_file):
        super().__init__(game_block)
        self.txt_file = txt_file

    def check_for_dup(self):
        with open(self.txt_file, "r", encoding="utf-8") as file:
            if self.game_name.a.text not in file.read():
                return False
            else:
                return True

    def log_game(self):
        with open(self.txt_file, "a", encoding="utf-8") as file:
            file.write(self.game_name.a.text + "\n")


class Tweeter(Website):
    def __init__(self, web):
        self.game_name = web.game_name
        self.steam_link = web.steam_link
        self.rank = web.rank

    def authorize_twitter(self):
        api_key = os.environ.get("twitter_api_key")
        api_secret = os.environ.get("twitter_api_key_secret")
        access_token = os.environ.get("twitter_access_token")
        access_secret = os.environ.get("twitter_access_token_secret")

        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_secret)

        self.api = tweepy.API(auth)

    def tweet(self):
        message = f"💎HIDDEN GEM OF THE DAY!💎\n\n🔥{self.game_name.a.text}🔥\n\nFind it here: {self.steam_link}\nFind more hidden gems: {self.rank}\n\n#gaming #games #steam #indiegame #indiegames"
        self.api.update_status(message)


def main():
    # Initialize some variables
    txt_file = "G:\\Python Projects\\Steam Hidden Gems Twitter\\GameList.txt"
    url = "https://steam250.com/hidden_gems"

    # Scrape the page
    site = requests.get(url)
    soup = bs4.BeautifulSoup(site.text, "lxml")

    game_num = random.randint(1, 250)
    game_block = soup.find("div", id=game_num)

    hidden_gems = Website(game_block)
    game_file = File(game_block, txt_file)

    while True:
        game_file.game()

        if game_file.check_for_dup():
            game_num = random.randint(1, 250)
            game_block = soup.find("div", id=game_num)
        else:
            break

    hidden_gems.game()
    hidden_gems.steam()
    hidden_gems.link()
    hidden_gems.ranking()

    steam_gems = Tweeter(hidden_gems)

    # Log the name of the game in the text file
    game_file.log_game()

    # Set up the link to twitter and post a tweet
    steam_gems.authorize_twitter()
    steam_gems.tweet()


if __name__ == "__main__":
    main()
