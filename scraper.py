import bs4 as bs
import urllib.request

steam_indie_games = urllib.request.urlopen("http://store.steampowered.com/tag/en/Indie/").read()
soup = bs.BeautifulSoup(steam_indie_games, 'lxml')

# Defining the initial source page
body = soup.body

# Set up the function to de-dupe the list of links we receive
def de_dupe(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


# Initialising a list we can use to store the game pages to visit

indie_game_list = []

# Retrieve the list of links, only for those that contain 'app'
for links in body.find_all('a'):
    link = links.get('href')
    if 'app' in link:
        print(link)
        indie_game_list.append(link)


# OLD:: For all the links we found on the page, visit them and add them to the list above
# for links in body.find_all('a'):
#     link = links.get('href')
#     indie_game_list.append(link)


# De-dupe the list and discard those that don't refer to game pages

de_dupe(indie_game_list)
print(indie_game_list)


# To Do Follow those links and collect the data for them


# links = soup.select("PopularNewReleasesRows a href")


# # for tabs in indie_page:
#     soup.find_all("div", {"class": "tab_item"})


# def game_details():
#     for games in indie_game_list:
#         follow_links = urllib.request.urlopen("http://store.steampowered.com/tag/en/Indie/").read()
#         soup = bs.BeautifulSoup(follow_links, 'lxml')
#         game_title = soup.find("div", {"class" : "apphub_AppName"})
#         game_desc = soup.find("div", {"class" : "game_description_snippet"})
#         print(game_title.string)
#         print(game_desc.string)

