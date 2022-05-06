from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/makegame/')
def generate_game():
    game_number = random.randint(3000, 7346)
    print(f'Get game {game_number} info')
    soup = BeautifulSoup(requests.get(f"https://j-archive.com/showgame.php?game_id={game_number}").content, 'html.parser')
    categories = soup.find_all('td', {'class': 'category_name'})

    all_categories = []
    all_clues = []
    try:
        for col in range(1, 13):
            this_category = []
            for row in range(1, 6):
                if col <= 6:
                    clue = soup.find(id=f'clue_J_{col}_{row}')
                else:
                    clue = soup.find(id=f'clue_DJ_{col - 6}_{row}')
                this_category.append(str(clue.text))
            all_categories.append(categories[col - 1].text)
            all_clues.append(this_category)
        return render_template('game.html', categories=all_categories, clues=all_clues)
    except Exception as e:
        return generate_game()
