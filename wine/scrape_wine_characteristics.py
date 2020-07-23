import requests
from bs4 import BeautifulSoup
import re


url = 'https://wine.lovetoknow.com/wine-beginners/wine-characteristics-glossary'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/76.0.3809.100 Safari/537.36'}
page = requests.get(url=url, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

mydivs = soup.findAll("strong")# [0].contents[0]

descriptors = []
for i in mydivs:
    content = i.contents[0]
    regex = r'\b(\w+)'
    content = re.findall(regex, content)[0]
    descriptors.append(content.lower())
print(descriptors)

desc = ['acidic', 'aggressive', 'alcoholic', 'angular', 'aroma', 'aromatic', 'astringent', 'austere', 'awkward', 'backbone', 'backward', 'balanced', 'big', 'bitter', 'blunt', 'body', 'bone', 'bouquet', 'brawny', 'briary', 'briny', 'brooding', 'buttery', 'chewy', 'clarity', 'clean', 'closed', 'cloudy', 'cloying', 'coarse', 'complex', 'creamy', 'delicate', 'dense', 'dry', 'earthy', 'elegant', 'fading', 'fat', 'finish', 'flabby', 'flat', 'fleshy', 'flinty', 'floral', 'forward', 'fresh', 'fruity', 'grassy', 'green', 'harsh', 'hearty', 'heavy', 'herbaceous', 'hollow', 'hot', 'jammy', 'lean', 'length', 'light', 'lush', 'masculine', 'meaty', 'medicinal', 'medium', 'metallic', 'moelleux', 'mouthfeel', 'nutty', 'oaky', 'off', 'peppery', 'perfumed', 'plummy', 'pruney', 'racy', 'raisiny', 'rich', 'robust', 'rustic', 'savory', 'short', 'silky', 'smoky', 'soft', 'spicy', 'steely', 'straw', 'structured', 'supple', 'sweet', 'tannic', 'tart', 'tight', 'toasty', 'umami', 'vegetal', 'velvety', 'vigorous', 'viscous', 'volatile', 'zesty']
colors = ['straw', 'yellow', 'gold', 'brown', 'amber', 'copper', 'salmon', 'pink', 'ruby', 'purple', 'garnet', 'tawny']
