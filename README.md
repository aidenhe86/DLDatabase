# Duel Links Card Database


#### <div align="center">Try It Here</div>
#### <div align="center">https://dl-card-deck.herokuapp.com/</div>

<br>
This website is aiming to help users to search YuGiOh Duel-Links Cards by card name, type, race, attribute, level, scale, attack and defense. Also users can create their decks in the website and share to other users.

#### User Flow
***
Card Search
1. User can click on the Card Search Area in the main page and direct to the card search page.
2. On top of the card search page, user can simply enter the card name to search. If user wants to enter more precise details, use the table below Card Name and enter card's type and race, if the card is monster card user can further enter card's attribute, level, scale, attack and defense.
3. Once user click search, the website will return the first 10 result by the informations user have entered.

Deck Build
1. If user have login, user can click on the Deck List Area in the main page and direct to the deck page. This page will show all the decks user have build.
2. On top of the deck page, click on the Create a New Deck button to create a new deck.
3. On the right side, user can search cards, click on the card and add it to their deck on the left side.
4. User can also click the card they have added in the deck to remove.
5. Once User complete their deck, click on submit and save the deck.

#### API LIST
***
[Yu-Gi-Oh! API by YGOPRODeck](https://db.ygoprodeck.com/api-guide/)

#### Technologies Used
***
* [Bootstrap](https://getbootstrap.com/)
* [Javascript](https://www.javascript.com/)
* [Python](https://www.python.org/)
* [Visual Studio Code](https://code.visualstudio.com/)
* [Heroku](https://www.heroku.com/)


#### Developments
***
To run the site locally,please follow the steps.
1. Clone the repository:
   git clone https://github.com/aidenhe86/capstone1.git

2. Download all require libraries.
   pip install -r requirements.txt

   (It may have issue when download psycopg2, please manually install psycopg2)
   pip install psycopg2-binary

3. Run command to run website locally.
   flask run