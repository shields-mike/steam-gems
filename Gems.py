import requests, bs4, datetime, pickle, random, os, tweepy, shutil


def game(game_block):
    """[This function takes in a BS4 Tag
        and finds a specific string within it]
    Args:
        game_block ([Beautiful Soup Tag]): [An object that corresponds to html
        tag in the document]

    Returns:
        [string]: [Returns the title of the game]
    """
    return game_block.find("span", class_="title")


def link(game_block):
    """[This function takes in a BS4 Tag
        and finds a specific string within it]
    Args:
        game_block ([Beautiful Soup Tag]): [An object that corresponds to html
        tag in the document]

    Returns:
        [string]: [Returns the steam 250 link of the game]
    """
    link_block = game_block.find("span", class_="title")
    return link_block.find("a")["href"]


def steam(game_block):
    """[This function takes in a BS4 Tag
        and finds a specific string within it]
    Args:
        game_block ([Beautiful Soup Tag]): [An object that corresponds to html
        tag in the document]

    Returns:
        [string]: [Returns the steam link of the game]
    """
    return game_block.find("a", class_="store")["href"]


def check_for_dup(game_name, txt_file):
    """[Checks whether or not the game is a duplicate]

    Args:
        game_name ([string]): [Title of the game]
        txt_file ([string]): [Path to where the file is stored]

    Returns:
        [boolean]: [Returns whether or not the game is a duplicate]
    """
    with open(txt_file, "r", encoding="utf-8") as file:
        if game_name.a.text not in file.read():
            return False
        else:
            return True


def log_game(game_name, txt_file):
    """[Writes the name of the game to the text file]

    Args:
        game_name ([string]): [Title of the game]
        txt_file ([string]): [Path to where the file is stored]
    """
    with open(txt_file, "a", encoding="utf-8") as file:
        file.write(game_name.a.text + "\n")


def ranking(link_250):
    """[Takes in a url and splits it on the '/'. It then concatenates it
        with another url]

    Args:
        link_250 ([string]): [The steam 250 link of the game]

    Returns:
        [string]: [New link that points to the game in the ranking list]
    """
    game_num = link_250.split("/")[4].strip()
    return f"https://steam250.com/hidden_gems#app/{game_num}"


def authorize_twitter():
    """[Takes in all the necessary requirements to authorize to twitter]

    Returns:
        [class]: [Returns the api needed to use twitter]
    """
    api_key = os.environ.get("twitter_api_key")
    api_secret = os.environ.get("twitter_api_key_secret")
    access_token = os.environ.get("twitter_access_token")
    access_secret = os.environ.get("twitter_access_token_secret")

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)

    return tweepy.API(auth)


def tweet(api, game_name, steam_link, rank):
    """[Tweet a message on twitter]

    Args:
        api ([class]): [API needed to use twitter]
        game_name ([string]): [Title of the game]
        steam_link ([string]): [Link to the steam page]
        rank ([string]): [Link to the game on the ranking list]
    """
    message = f"💎HIDDEN GEM OF THE DAY!💎\n\n🔥{game_name.a.text}🔥\n\nFind it here: {steam_link}\nFind more hidden gems: {rank}\n\n#gaming #hiddengems #steam #indiegame #steam250"
    api.update_status(message)


def main():
    # Initialize some variables
    dup = True
    txt_file = "G:\\Python Projects\\Steam Hidden Gems Twitter\\GameList.txt"
    url = "https://steam250.com/hidden_gems"

    # Scrape the page
    site = requests.get(url)
    soup = bs4.BeautifulSoup(site.text, "lxml")

    # While loop to check if the game is a duplicate
    while dup:
        game_num = random.randint(1, 250)
        game_block = soup.find("div", id=game_num)

        game_name = game(game_block)
        steam_link = steam(game_block)
        link_250 = link(game_block)
        rank = ranking(link_250)

        dup = check_for_dup(game_name, txt_file)

    # Log the name of the game in the text file
    log_game(game_name, txt_file)

    # Set up the link to twitter and post a tweet
    api = authorize_twitter()
    tweet(api, game_name, steam_link, rank)


if __name__ == "__main__":
    main()
