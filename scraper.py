import bs4 as bs
from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome(executable_path=r"/home/james/beautifulsoup/chromedriver")
browser.get("http://store.steampowered.com/tag/en/Indie/")
html_source = browser.page_source
soup = bs.BeautifulSoup(html_source, 'lxml')

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
# In the future i could try and remove the params
for links in body.find_all('a', href=True):
    link = links.get('href')
    if 'app' in link:
        indie_game_list.append(link)


# De-dupe the list and discard those that don't refer to game pages
de_dupe(indie_game_list)
print(indie_game_list[3:])


# Follow those links, minus the first three to Steam hardware, and collect the data for them
for target in indie_game_list[3:]:
    browser.get(str(target))
    print(str(target))
    # Using Selenium to click the Continue button on age check if triggered
    game_page = browser.page_source
    if 'agecheck' in browser.current_url:
        btn = browser.find_element_by_link_text("Continue")
        browser.implicitly_wait(5)
        btn.click()
        game_page = browser.page_source
    soup = bs.BeautifulSoup(game_page, 'lxml')
    body = soup.body
    game_title = soup.find("div", {"class" : "apphub_AppName"})
    game_desc = soup.find("div", {"class" : "game_description_snippet"})
    if game_title:
        print(game_title.string)
    else:
        print("No Title")
    if game_desc:
        print(game_desc.string)
    else:
        print("No Description")

browser.quit()

# Create a list where each value is a dictionary of title and description values
