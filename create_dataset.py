import pickle
import json
import csv
import pandas as pd
import re

"""
Replace the text of a card with a text to be analysed.

Example input:
[x]Deal $4 damage.\nDiscard a random card.
Output:
deal 4 damage discard a random card
"""
def clean_text(df, index):

    text = df.iloc[index, df.columns.get_loc('text')]

    if pd.isna(text):
        pass
    else:
        text = text.replace('<i>','')
        text = text.replace('</i>','')
        text = text.replace('<b>','')
        text = text.replace('</b>','')
        text = text.replace('\\n',' ')
        text = text.replace('[x]','')

        text = re.sub(r'[\W_]+', ' ', text)
        text = text.lower()

    df.iloc[index, df.columns.get_loc('text')] = text

"""
Prepare the data to be analysed
"""
def prepare_data(df, index):

    collectible = df.iloc[index, df.columns.get_loc('collectible')]
    armor = df.iloc[index, df.columns.get_loc('armor')]
    elite = df.iloc[index, df.columns.get_loc('elite')]
    faction = df.iloc[index, df.columns.get_loc('faction')]
    race = df.iloc[index, df.columns.get_loc('race')]
    howToGet = df.iloc[index, df.columns.get_loc('howToGet')]
    howToGetGold = df.iloc[index, df.columns.get_loc('howToGetGold')]
    durability = df.iloc[index, df.columns.get_loc('durability')]
    mechanics = df.iloc[index, df.columns.get_loc('mechanics')]
    health = df.iloc[index, df.columns.get_loc('health')]
    attack = df.iloc[index, df.columns.get_loc('attack')]

    if pd.isna(howToGetGold):
        df.iloc[index, df.columns.get_loc('howToGetGold')] = False
    else:
        df.iloc[index, df.columns.get_loc('howToGetGold')] = True
    if pd.isna(howToGet):
        df.iloc[index, df.columns.get_loc('howToGet')] = False
    else:
        df.iloc[index, df.columns.get_loc('howToGet')] = True
    if pd.isna(race):
        df.iloc[index, df.columns.get_loc('race')] = 'None'
    if pd.isna(faction):
        df.iloc[index, df.columns.get_loc('faction')] = 'None'
    if pd.isna(elite):
        df.iloc[index, df.columns.get_loc('elite')] = False
    if pd.isna(collectible):
        df.iloc[index, df.columns.get_loc('collectible')] = False
    if pd.isna(armor):
        df.iloc[index, df.columns.get_loc('armor')] = 0.0
    if pd.isna(durability):
        df.iloc[index, df.columns.get_loc('durability')] = 0.0
    if pd.isna(mechanics):
        df.iloc[index, df.columns.get_loc('mechanics')] = 'None'
    if pd.isna(health):
        df.iloc[index, df.columns.get_loc('health')] = 0.0
    if pd.isna(attack):
        df.iloc[index, df.columns.get_loc('attack')] = 0.0

"""
The 'machanics' field needs more preparation because of its composition.

Example input:
[{'name': 'Magnetic'}, {'name': 'Divine Shield'}]
Output:
Magnetic,Divine Shield
"""
def clean_mechanics(df, index):

    mechanic = df.iloc[index, df.columns.get_loc('mechanics')]

    if not pd.isna(mechanic):
        mechanic = mechanic.replace("[{'name': '","")
        mechanic = mechanic.replace("'}]","")
        mechanic = mechanic.replace("'}, {'name': '",",")
        df.iloc[index, df.columns.get_loc('mechanics')] = mechanic

"""
Encoding of the 'mechanics' to other column fields.
Valuing the 'number mechanics' field.

Example input:
Magnetic,Divine Shield
Output:
... | Magnetic |  ...  | Divine Shield |  ...  | number mechanics
... | True     | False | True          | False | 2

"""
def encode_mechanics(df, index):

    # All False
    for token in mechanics:
        df.iloc[index, df.columns.get_loc(token)] = False

    # Some True
    mechanic = df.iloc[index, df.columns.get_loc('mechanics')]

    if pd.isna(mechanic):
        pass
    else:
        mechanic = mechanic.split(',')
        for token in mechanic:
            df.iloc[index, df.columns.get_loc(token)] = True

    # Number mechanics
    count = 0
    for token in mechanics:
        if df.iloc[index, df.columns.get_loc(token)]:
            count +=1
    df.iloc[index, df.columns.get_loc('number mechanics')] = count


"""
delete unuseful rows. Basically, there are too many cards because
the most of the rows refers to cards not in the collection, generated
cards (like lackeys) or to specific dynamics of the game.
"""
def delete_rows(df):

    df = df.drop(df[df.img.isna()].index)
    df = df.drop(df[df.cost.isna()].index)
    df = df.drop(df[df.rarity.isna()].index)
    return df

"""
Read the json file containing all the cards and save it as a csv format file
"""
def json2csv():

    # json to dictionary
    file = open('all_json', 'rb')
    json_data = pickle.load(file)
    all_cards = json.loads(json_data)
    file.close()

    # Write csv
    with open('cards.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, delimiter=';', fieldnames=header)
        writer.writeheader()

        # for each card
        for set in sets:
            for card in all_cards[set]:
                # 6463 cards
                writer.writerow(card)

def main():

    print('Computing... It may take some time...')

    json2csv()
    df = pd.read_csv('cards.csv', delimiter=';', names=header, header=0)
    df = delete_rows(df)

    # for each row
    for index in range(len(df)):
        clean_mechanics(df, index)
        encode_mechanics(df, index)
        prepare_data(df, index)
        clean_text(df, index)
    df.to_csv("cards.csv", index=False, sep=";")

# card sets
file = open('card_sets.txt', 'r')
sets = file.read().splitlines()
file.close()

# card attributes
file = open('header.txt', 'r')
header = file.read().splitlines()
file.close()

# card mechanics
file = open('mechanics.txt', 'r')
mechanics = file.read().splitlines()
file.close()

if __name__ == '__main__':
    main()
