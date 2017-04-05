import bs4 as bs
import urllib.request

# "http://store.steampowered.com/app/493340/"
steam_indie_games = urllib.request.urlopen("http://store.steampowered.com/tag/en/Indie/").read()
soup = bs.BeautifulSoup(steam_indie_games, 'lxml')


body = soup.body

for links in body.find_all('a'):
    print(links.get('href'))


# links = soup.select("PopularNewReleasesRows a href")


# # for tabs in indie_page:
#     soup.find_all("div", {"class": "tab_item"})



# def titles_and_desc():
#     for games in indie_game_list:
#
#         game_title = soup.find("div", {"class" : "apphub_AppName"})
#         game_desc = soup.find("div", {"class" : "game_description_snippet"})
#         print(game_title.string)
#         print(game_desc.string)

