import pandas as pd
import re
from helpers import common_words


desc = ['acidic', 'aggressive', 'alcoholic', 'angular', 'aroma', 'aromatic', 'astringent', 'austere', 'awkward', 'backbone', 'backward', 'balanced', 'big', 'bitter', 'blunt', 'body', 'bone', 'bouquet', 'brawny', 'briary', 'briny', 'brooding', 'buttery', 'chewy', 'clarity', 'clean', 'closed', 'cloudy', 'cloying', 'coarse', 'complex', 'creamy', 'delicate', 'dense', 'dry', 'earthy', 'elegant', 'fading', 'fat', 'finish', 'flabby', 'flat', 'fleshy', 'flinty', 'floral', 'forward', 'fresh', 'fruity', 'grassy', 'green', 'harsh', 'hearty', 'heavy', 'herbaceous', 'hollow', 'hot', 'jammy', 'lean', 'length', 'light', 'lush', 'masculine', 'meaty', 'medicinal', 'medium', 'metallic', 'moelleux', 'mouthfeel', 'nutty', 'oaky', 'off', 'peppery', 'perfumed', 'plummy', 'pruney', 'racy', 'raisiny', 'rich', 'robust', 'rustic', 'savory', 'short', 'silky', 'smoky', 'soft', 'spicy', 'steely', 'straw', 'structured', 'supple', 'sweet', 'tannic', 'tart', 'tight', 'toasty', 'umami', 'vegetal', 'velvety', 'vigorous', 'viscous', 'volatile', 'zesty']
colors = ['straw', 'yellow', 'gold', 'brown', 'amber', 'copper', 'salmon', 'pink', 'ruby', 'purple', 'garnet', 'tawny']


def _create_color_table(to_csv=False):
    df_colors = pd.DataFrame(colors, columns=['ColorDesc'])
    df_colors['ColorID'] = df_colors.index
    df_colors = df_colors[['ColorID', 'ColorDesc']]
    print(df_colors)
    if to_csv:
        df_colors.to_csv('./data/color_table.csv')


def _create_descriptor_table(to_csv=False):
    df_descriptors = pd.DataFrame(desc, columns=['DescriptorDesc'])
    df_descriptors['DescriptorID'] = df_descriptors.index
    df_descriptors = df_descriptors[['DescriptorID', 'DescriptorDesc']]
    print(df_descriptors)
    if to_csv:
        df_descriptors.to_csv('./data/descriptor_table.csv')


def _create_region_table(to_csv=False):
    df = pd.read_csv('./data/wine_full.csv', encoding="ISO-8859-1")
    df_pairs = df[['Region', 'Country']]
    df_pairs = df_pairs.drop_duplicates()  # Some questionable pairs near the end. Include for now.

    df_country = pd.read_csv('./data/country_table.csv', encoding="ISO-8859-1")
    country_id = []
    for country in df_pairs['Country']:
        country_id.append(int(df_country.loc[df_country['CountryDesc'] == country]['CountryID']))
    df_pairs['CountryID'] = country_id
    df_regions = df_pairs.reset_index(drop=True)
    df_regions['RegionID'] = df_regions.index
    df_regions['RegionDesc'] = df_regions['Region']
    df_regions = df_regions[['RegionID', 'RegionDesc', 'CountryID']]

    if to_csv:
        df_regions.to_csv('./data/region_table.csv')


def _create_country_table(to_csv=False):
    df = pd.read_csv('./data/wine_full.csv', encoding="ISO-8859-1")
    countries = df.Country.unique()
    df_countries = pd.DataFrame(countries, columns=['CountryDesc'])
    df_countries['CountryID'] = df_countries.index
    df_countries = df_countries[['CountryID', 'CountryDesc']]
    print(df_countries)
    if to_csv:
        df_countries.to_csv('./data/country_table.csv')


def _create_variety_table(to_csv=False):
    df = pd.read_csv('./data/wine_full.csv', encoding="ISO-8859-1")
    varieties = df.Variety.unique()
    new_varieties = []
    for variety in varieties:
        wine_varieties = variety.split(',')
        for wine_variety in wine_varieties:
            if wine_variety and wine_variety not in new_varieties:
                new_varieties.append(wine_variety)
    df_varieties = pd.DataFrame(new_varieties, columns=['VarietyDesc'])
    df_varieties['VarietyID'] = df_varieties.index
    df_varieties = df_varieties[['VarietyID', 'VarietyDesc']]
    if to_csv:
        df_varieties.to_csv('./data/variety_table.csv')


def _create_winename_table(to_csv=False):
    df = pd.read_csv('./data/wine_full.csv', encoding="ISO-8859-1")
    df_winename = df[['Name', 'Vintage']]
    df_winename['WineID'] = df_winename.index
    df_winename = df_winename[['WineID', 'Name', 'Vintage']]
    df_winename = df_winename.rename(columns={'Name': 'WineDesc'})
    print(df_winename.head(10))
    if to_csv:
        df_winename.to_csv('./data/winename_table.csv')


def _create_variety_relationship_table(to_csv=False):
    df = pd.read_csv('./data/wine_full_char.csv', encoding="ISO-8859-1")
    df_name = pd.read_csv('./data/winename_table.csv', encoding="ISO-8859-1")[['WineID', 'WineDesc']]
    df_variety = pd.read_csv('./data/variety_table.csv', encoding="ISO-8859-1")

    df_variety_relationship = pd.DataFrame(columns=['WineID', 'VarietyID'])
    for index, row in df[['Name', 'Variety']].iterrows():
        if type(row['Variety']) is not float and row['Name'] != 'nan' and type(row['Name']) is not float:
            wine_varieties = row['Variety'].split(',')
            for wine_variety in wine_varieties:
                try:
                    # print(row['Name'], type(row['Name']), row['Variety'], type(row['Variety']))
                    wines_with_variety = df_name.loc[df_name['WineDesc'] == row['Name']]
                    wine_id = wines_with_variety['WineID'].to_numpy()[0]
                    variety_id = df_variety.loc[df_variety['VarietyDesc'] == wine_variety]['VarietyID'].to_numpy()[0]
                    df_variety_relationship = df_variety_relationship.append(
                        {'WineID': wine_id, 'VarietyID': variety_id}, ignore_index=True
                    )
                except Exception as e:
                    print(f'!!Exception!! {e} on {row["Name"]} with {wine_variety}')
                    pass
    df_variety_relationship['VRelationshipID'] = df_variety_relationship.index
    df_variety_relationship = df_variety_relationship[['VRelationshipID', 'WineID', 'VarietyID']]
    print(df_variety_relationship)
    if to_csv:
        df_variety_relationship.to_csv('./data/variety_relationships_table.csv')


def _create_color_relationship_table(to_csv=False):
    df = pd.read_csv('./data/wine_full_char.csv', encoding="ISO-8859-1")
    df_name = pd.read_csv('./data/winename_table.csv', encoding="ISO-8859-1")[['WineID', 'WineDesc']]
    df_color = pd.read_csv('./data/color_table.csv', encoding="ISO-8859-1")

    df_color_relationship = pd.DataFrame(columns=['WineID', 'ColorID'])
    for index, row in df[['Name', 'Colors']].iterrows():
        if type(row['Colors']) is not float:
            wines_with_color = df_name.loc[df_name['WineDesc'] == row['Name']]
            wine_id = wines_with_color['WineID'].to_numpy()[0]
            color_list = re.sub("[^\w]", " ",  row['Colors']).split()
            for color in color_list:
                color_id = df_color.loc[df_color['ColorDesc'] == color]['ColorID'].to_numpy()[0]
                df_color_relationship = df_color_relationship.append(
                    {'WineID': wine_id, 'ColorID': color_id}, ignore_index=True
                )
    df_color_relationship['CRelationshipID'] = df_color_relationship.index
    df_color_relationship = df_color_relationship[['CRelationshipID', 'WineID', 'ColorID']]
    if to_csv:
        df_color_relationship.to_csv('./data/color_relationships_table.csv')


def _create_description_relationship_table(to_csv=False):
    df = pd.read_csv('./data/wine_full_char.csv', encoding="ISO-8859-1")
    df_name = pd.read_csv('./data/winename_table.csv', encoding="ISO-8859-1")[['WineID', 'WineDesc']]
    df_descriptor = pd.read_csv('./data/descriptor_table.csv', encoding="ISO-8859-1")

    df_descriptor_relationship = pd.DataFrame(columns=['WineID', 'DescriptorID'])
    for index, row in df[['Name', 'Descriptors']].iterrows():
        if type(row['Descriptors']) is not float:
            wines_with_descriptor = df_name.loc[df_name['WineDesc'] == row['Name']]
            wine_id = wines_with_descriptor['WineID'].to_numpy()[0]
            descriptor_list = re.sub("[^\w]", " ",  row['Descriptors']).split()
            for descriptor in descriptor_list:
                descriptor_id = df_descriptor.loc[df_descriptor['DescriptorDesc'] == descriptor]['DescriptorID'].to_numpy()[0]
                df_descriptor_relationship = df_descriptor_relationship.append(
                    {'WineID': wine_id, 'DescriptorID': descriptor_id}, ignore_index=True
                )
    df_descriptor_relationship['DRelationshipID'] = df_descriptor_relationship.index
    df_descriptor_relationship = df_descriptor_relationship[['DRelationshipID', 'WineID', 'DescriptorID']]
    if to_csv:
        df_descriptor_relationship.to_csv('./data/descriptor_relationships_table.csv')


def _compare_add_desc(to_csv=False):
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

    if to_csv:
        df.drop(columns='ComboDesc', inplace=True)
        df.to_csv('wine_full_char.csv')
