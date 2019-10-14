# What-Makes-a-Hearthstone-Card-Legendary
Tree-based machine learning approach to identify the characteristics of legendary card

## Project Description
Hearthstone is a complex card game with several mechanics and an ever-evolving metagame. Even if trending decks change and strategies mutate, there are some powerful legendary cards that remain popular over the time.

But, exactly, what makes a card legendary? In this project, I want to answer this question with the help of Machine Learning and all the cards published during the life of the game. Using the Random Forest algorithm, I predict the rarity of a card based on the characteristics of the card itself and rank their importance in determining whether a card is classified as legendary.

## Dataset
It is possible to download the full dataset of the cards from the [Hearthstone API website](https://hearthstoneapi.com/) as a JSON. Once the file is received and saved in the pickle format, the script `create_dataset.py` turns it into a csv. At the link it is possible to find the description of the attributes of each card.

## Cards Analysis
Even if the legendary cards are always powerful, some of them express their full potential only in particular situations. This is why it is possible to divide the cards in two main groups: cards like [Zilliax](http://media.services.zam.com/v1/media/byName/hs/cards/enus/BOT_548.png), for example, are played in almost each archetype; others, like [Kathrena Winterwisp](http://media.services.zam.com/v1/media/byName/hs/cards/enus/LOOT_511.png), are only played in a well defined situations. Unfortunately, the most of the legendary cards is from the second type. Moreover, similar cards may have different rarity rank. This is the case of [Baron Rivendare](http://media.services.zam.com/v1/media/byName/hs/cards/enus/FP1_031.png) and [Necromechanic](http://media.services.zam.com/v1/media/byName/hs/cards/enus/BOT_039.png), which share the same card text. Usually, cards with strong game dynamics do not have high statistics to compensate their effect: it is the case of [Azalina Soulthief](http://media.services.zam.com/v1/media/byName/hs/cards/enus/GIL_198.png).

## Results
The results, as presented in the file `classifier.ipynb`, show a high importance of few attributes:
1. cost (22%)
2. health (17%)
3. attack (16%)
4. race (6%)
5. number mechanics (6%)
