import pandas as pd


def common_words(a, b):
    a_set = set(a)
    b_set = set(b)

    if a_set & b_set:
        return a_set & b_set
    else:
        return None

desc = ['acidic', 'aggressive', 'alcoholic', 'angular', 'aroma', 'aromatic', 'astringent', 'austere', 'awkward', 'backbone', 'backward', 'balanced', 'big', 'bitter', 'blunt', 'body', 'bone', 'bouquet', 'brawny', 'briary', 'briny', 'brooding', 'buttery', 'chewy', 'clarity', 'clean', 'closed', 'cloudy', 'cloying', 'coarse', 'complex', 'creamy', 'delicate', 'dense', 'dry', 'earthy', 'elegant', 'fading', 'fat', 'finish', 'flabby', 'flat', 'fleshy', 'flinty', 'floral', 'forward', 'fresh', 'fruity', 'grassy', 'green', 'harsh', 'hearty', 'heavy', 'herbaceous', 'hollow', 'hot', 'jammy', 'lean', 'length', 'light', 'lush', 'masculine', 'meaty', 'medicinal', 'medium', 'metallic', 'moelleux', 'mouthfeel', 'nutty', 'oaky', 'off', 'peppery', 'perfumed', 'plummy', 'pruney', 'racy', 'raisiny', 'rich', 'robust', 'rustic', 'savory', 'short', 'silky', 'smoky', 'soft', 'spicy', 'steely', 'straw', 'structured', 'supple', 'sweet', 'tannic', 'tart', 'tight', 'toasty', 'umami', 'vegetal', 'velvety', 'vigorous', 'viscous', 'volatile', 'zesty']
colors = ['straw', 'yellow', 'gold', 'brown', 'amber', 'copper', 'salmon', 'pink', 'ruby', 'purple', 'garnet', 'tawny']

df = pd.read_csv('./data/wine_full.csv', encoding="ISO-8859-1")
df['ComboDesc'] = df['TastingNotes'].astype(str) + ' ' + df['Review'].astype(str)

descriptors = []
color = []

for index, note in df['ComboDesc'].items():
    try:
        note_clean = note.lower().replace(',', '').replace('.', '').split(' ')
        if common_words(note_clean, desc):
            descriptors.append(list(common_words(note_clean, desc)))
        else:
            descriptors.append(None)
        if common_words(note_clean, colors):
            color.append(list(common_words(note_clean, colors)))
        else:
            color.append(None)
    except AttributeError:
        descriptors.append(None)
        color.append(None)

df['Descriptors'] = descriptors
df['Colors'] = color

df.drop(columns='ComboDesc', inplace=True)
# df.to_csv('wine_full_char.csv')

