import bs4 as bs
from selenium import webdriver
from selenium.webdriver.support.ui import Select
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


# Create a new empty list, which will store dictionaries of our data
game_titles_and_desc = []


# Follow those links, minus the first three to Steam hardware, and collect the data for them
for target in indie_game_list[3:]:
    browser.get(str(target))
    # Create a new dictionary for each target
    game_dict = {'url': str(target)}
    # Using Selenium to handle the age check button / form if triggered
    game_page = browser.page_source
    if 'agecheck' in browser.current_url:
        btn = browser.find_elements_by_link_text("Continue")
        form = browser.find_elements_by_id("agecheck_form")
        if len(btn) > 0 and btn[0].is_displayed():
            browser.implicitly_wait(5)
            btn[0].click()
            game_page = browser.page_source
        elif len(form) > 0 and form[0].is_displayed():
            select_day = Select(browser.find_element_by_name('ageDay'))
            select_day.select_by_value('10')
            select_month = Select(browser.find_element_by_name('ageMonth'))
            select_month.select_by_value('May')
            select_year = Select(browser.find_element_by_name('ageYear'))
            select_year.select_by_value('1980')
            game_page = browser.page_source
            enter = browser.find_element_by_link_text("Enter")
            browser.implicitly_wait(5)
            enter.click()
        else:
            print("Age Check barrier")
            continue
    # Now we have the actual game page, get the title and description
    soup = bs.BeautifulSoup(game_page, 'lxml')
    body = soup.body
    game_title = soup.find("div", {"class" : "apphub_AppName"})
    game_desc = soup.find("div", {"class" : "game_description_snippet"})
    # Where they exist, add them to the instance disctionary
    if game_title:
        game_dict['title'] = game_title.text.replace("\n", "").replace("\t", "")
    else:
        print("No Title")
    if game_desc:
        game_dict['desc'] = game_desc.text.replace("\n", "").replace("\t", "")
    else:
        print("No Description")
    # Finally add the target's dictionary of data to the master list
    game_titles_and_desc.append(game_dict)

browser.quit()

# Show all the data we've gathered
print(game_titles_and_desc)
