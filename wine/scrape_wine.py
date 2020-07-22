import requests
from bs4 import BeautifulSoup, element
import re
import time
import pandas as pd


url_xml = 'https://www.thewinebuyer.com/sitemap.xml'
url = 'https://www.thewinebuyer.com/sku39013.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/76.0.3809.100 Safari/537.36'}
r = requests.get(url=url_xml, headers=headers)
xml = r.text

soup = BeautifulSoup(xml, 'html.parser')
sitemapTags = soup.find_all("loc")

skus = []
for tag in sitemapTags:
    url_sku = tag.contents[0]
    sku = re.findall('^HTTP://www.thewinebuyer.com/sku(.*).html', url_sku)
    if len(sku) > 0:
        skus.append('https://www.thewinebuyer.com/sku' + str(sku[0]) + '.html')

skus = skus[1020:1025]

toCSV = []
setting = 'DEBUG'   # 'RUN'
for url in skus:
    time.sleep(1)
    print('URL: ' + str(url))
    new_dict = {}
    try:
        page = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')
        mydivs = soup.findAll("span", {"class": "iteminfo"})

        # Name
        name = soup.findAll("span", {"class": "producttitle"})[0]
        if setting == 'DEBUG':
            print('Name: ' + str(name.contents[0]))
        if setting == 'RUN':
            new_dict['Name'] = str(name.contents[0])

        # Vintage:
        try:
            vintage = soup.findAll("span", {"class": "vintage"})[0]
            if setting == 'DEBUG':
                print('Vintage: ' + str(vintage.contents[0]))
            if setting == 'RUN':
                new_dict['Vintage'] = str(vintage.contents[0])
        except (IndexError, NameError):
            if setting == 'RUN':
                new_dict['Vintage'] = None
            pass

        # Variety
        variety = soup.select("a[href*=sel_variety]")[-1]
        if setting == 'DEBUG':
            print('Variety: ' + str(variety.contents[0]))
        if setting == 'RUN':
            new_dict['Variety'] = str(variety.contents[0])

        # Country
        try:
            for y in mydivs:
                if len(y.select("a[href*=country]")) > 0:
                    country_href = y
                    break
            country = country_href.contents[0].contents[0]
            if setting == 'DEBUG':
                print('Country: ' + str(country))
            if setting == 'RUN':
                new_dict['Country'] = str(country)
        except (IndexError, NameError):
            if setting == 'RUN':
                new_dict['Country'] = None
            pass

        # Region
        try:
            for z in mydivs:
                if len(z.select("a[href*=®ion]")) > 0:
                    region_href = z
                    break
            region = region_href.contents[0].contents[0]
            if setting == 'DEBUG':
                print('Region: ' + str(region))
            if setting == 'RUN':
                new_dict['Region'] = str(region)
        except (IndexError, NameError):
            if setting == 'RUN':
                new_dict['Region'] = None
            pass

        # Subregion
        try:
            subregion = soup.select("a[href*=subregion]")[0]
            if setting == 'DEBUG':
                print('Subregion: ' + str(subregion.contents[0]))
            if setting == 'RUN':
                new_dict['Subregion'] = str(subregion.contents[0])
        except (IndexError, NameError):
            if setting == 'RUN':
                new_dict['Subregion'] = None
            pass

        # Appellation
        try:
            appellation = soup.select("a[href*=appellation]")[0]
            if setting == 'DEBUG':
                print('Appellation: ' + str(appellation.contents[0]))
            if setting == 'RUN':
                new_dict['Appellation'] = str(appellation.contents[0])
        except (IndexError, NameError):
            if setting == 'RUN':
                new_dict['Appellation'] = None
            pass

        # Tasting Notes:
        try:
            topics = soup.findAll("span", {"class": "topic"})
            tasting_notes_list = []
            for i in topics:
                if i.contents[0] == 'Tasting Notes' or i.contents[0] == 'Tasting notes':
                    tasting_notes_list.append(i)
            if len(tasting_notes_list) == 0:
                raise NameError
            else:
                tasting_notes = tasting_notes_list[0]
            tasting_notes_desc = tasting_notes.findNext('tr').findChildren("td", recursive=False)[0].contents
            full_tasting_notes_desc = ""
            for note in tasting_notes_desc:
                if note != 'This content belongs to bevnetwork.com and THEWINEBUYER' and \
                        note != '<!--This content belongs to bevnetwork.com and THEWINEBUYER-->':
                    full_tasting_notes_desc += str(note)

            if setting == 'DEBUG':
                print('Tasting Notes: ' + str(full_tasting_notes_desc))
            if setting == 'RUN':
                new_dict['TastingNotes'] = str(full_tasting_notes_desc)

            descriptors = ['acidic', 'aggressive', 'alcoholic', 'angular', 'aroma', 'aromatic', 'astringent', 'austere', 'awkward', 'backbone', 'backward', 'balanced', 'big', 'bitter', 'blunt', 'body', 'bone', 'bouquet', 'brawny', 'briary', 'briny', 'brooding', 'buttery', 'chewy', 'clarity', 'clean', 'closed', 'cloudy', 'cloying', 'coarse', 'complex', 'creamy', 'delicate', 'dense', 'dry', 'earthy', 'elegant', 'fading', 'fat', 'finish', 'flabby', 'flat', 'fleshy', 'flinty', 'floral', 'forward', 'fresh', 'fruity', 'grassy', 'green', 'harsh', 'hearty', 'heavy', 'herbaceous', 'hollow', 'hot', 'jammy', 'lean', 'length', 'light', 'lush', 'masculine', 'meaty', 'medicinal', 'medium', 'metallic', 'moelleux', 'mouthfeel', 'nutty', 'oaky', 'off', 'peppery', 'perfumed', 'plummy', 'pruney', 'racy', 'raisiny', 'rich', 'robust', 'rustic', 'savory', 'short', 'silky', 'smoky', 'soft', 'spicy', 'steely', 'straw', 'structured', 'supple', 'sweet', 'tannic', 'tart', 'tight', 'toasty', 'umami', 'vegetal', 'velvety', 'vigorous', 'viscous', 'volatile', 'zesty']
            wine_descriptors = ""
            for word in full_tasting_notes_desc.split():
                if word.lower() in descriptors:
                    wine_descriptors += " " + str(word.lower())

        except (IndexError, NameError):
            if setting == 'RUN':
                new_dict['TastingNotes'] = None
            pass

        # Review & Rating
        try:
            topics = soup.findAll("span", {"class": "topic"})
            rating_title_list = []
            for i in topics:
                if i.contents[0] == 'Rating':
                    rating_title_list.append(i)
            if len(rating_title_list) == 0:
                raise NameError
            else:
                rating_title = rating_title_list[0]

            rating_desc = rating_title.findNext('tr').findChildren("td", recursive=False)[0].contents[0]
            while type(rating_desc) != element.NavigableString:
                rating_desc = rating_desc.contents[0]
            if setting == 'DEBUG':
                print('Review: ' + str(rating_desc))
            if setting == 'RUN':
                new_dict['Review'] = str(rating_desc)

            rating_source_value = rating_title.findNext('tr').findChildren("td", recursive=False)[0] \
                .findChildren("b", recursive=True)[0].contents[0]

            rating_source = str(rating_source_value).split(',')[0]
            if setting == 'DEBUG':
                print('- ' + str(rating_source))
            rating_value = str(rating_source_value).split(' ')
            for j in rating_value:
                if j.isdigit():
                    rating_value_int = j
            if setting == 'DEBUG':
                print(str(rating_value_int) + ' Points')
            if setting == 'RUN':
                new_dict['Rating'] = str(rating_value_int)
        except (IndexError, NameError):
            if setting == 'RUN':
                new_dict['Review'] = None
                new_dict['Rating'] = None
            pass

        # Price
        try:
            price = soup.findAll("span", {"class": "RegularPrice"})
            price = price[0].contents[0]
            price_float = re.findall(r"\$(\d+\.\d+)", price)[0]
            if setting == 'DEBUG':
                print('Price: ' + str(price_float))
            if setting == 'RUN':
                new_dict['Price'] = str(price)
        except (IndexError, NameError):
            if setting == 'RUN':
                new_dict['Price'] = None
            pass

        toCSV.append(new_dict)
    except Exception as e:
        print('ERROR! ' + str(e))
        pass
if setting == 'RUN':
    toCSV_pd = pd.DataFrame(toCSV)
    toCSV_pd.to_csv(r'C:\Users\AlyshaHelenic\Desktop\export_dataframe.csv', index=None, header=True)
