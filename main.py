from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import uuid
import openai
import requests
import pystache


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

jwt = JWTManager(app)

# Configure your JWT Secret Key
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# Set your OpenAI API key here
openai.api_key = 'your-api-key'

# Your ElevenLabs API key
elevenlabs_api_key = 'your_elevenlabs_api_key'


def generate_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-004",  # or the latest available engine
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

def render_template(file_name, context):
    with open(file_name, 'r') as file:
        template = file.read()
    return pystache.render(template, context)


games = {}  # Store game data


# Endpoint to create a new game
@app.route('/create-game', methods=['POST'])
def create_game():
    host_email = request.json.get('host_email')
    game_id = str(uuid.uuid4())
    games[game_id] = {
        'host': host_email,
        'players': [],
        'status': 'created',
        'round': 1,
        'character_assignments': {},
    }

    access_token = create_access_token(identity=host_email)
    return jsonify({'game_id': game_id, 'token': access_token})

# Endpoint to advance the game, accessible only by the host
@app.route('/advance-game', methods=['POST'])
@jwt_required()
def advance_game():
    game_id = request.json.get('game_id')
    host_email = get_jwt_identity()

    if game_id in games and games[game_id]['host'] == host_email:
        games[game_id]['round'] += 1
        return jsonify({'status': 'game advanced to round', 'round': games[game_id]['round']})
    else:
        return jsonify({'error': 'Unauthorized or Game not found'}), 403


def get_storyline_for_act(game_id, act):
    game = games.get(game_id)
    if game and act in game['storyline']:
        return game['storyline'][act]
    return "Storyline not found for this act."

# Endpoint to get narrated storyline
@app.route('/narrate-storyline', methods=['POST'])
def narrate_storyline():
    game_id = request.json.get('game_id')
    act = request.json.get('act')

    if game_id in games:
        storyline = get_storyline_for_act(game_id, act)  # Implement this function based on your game logic
        audio_url = generate_narration(storyline)
        return jsonify({'audio_url': audio_url})
    else:
        return jsonify({'error': 'Game not found'}), 404

def generate_narration(text):
    url = 'https://api.elevenlabs.io/synthesize'
    headers = {'Authorization': f'Bearer {elevenlabs_api_key}'}
    payload = {
        'text': text,
        'voice': 'your_preferred_voice'  # Choose a voice from ElevenLabs offerings
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json().get('audioUrl')
    else:
        return 'Error generating narration'

@app.route('/theme-selection', methods=['POST'])
def theme_selection():
    theme = request.json.get('theme')
    prompt = render_template('prompts/theme_selection.prompt', {'theme': theme})
    response = generate_response(prompt)
    return jsonify({'details': response})


@app.route('/setting-time-period', methods=['POST'])
def setting_time_period():
    theme = request.json.get('theme')
    prompt = f"Describe the setting and time period for a murder mystery game based on the theme '{theme}'. Include details about the environment, cultural context, and historical elements relevant to this theme."
    response = generate_response(prompt)
    return jsonify({'setting_time_period': response})


@app.route('/main-plot-outline', methods=['POST'])
def main_plot_outline():
    theme = request.json.get('theme')
    prompt = f"Create a basic plot outline for a murder mystery game with the theme '{theme}'. Detail the central event, the reason for the gathering, and the victim's role in the story."
    response = generate_response(prompt)
    return jsonify({'plot_outline': response})


@app.route('/character-creation', methods=['POST'])
def character_creation():
    theme = request.json.get('theme')
    prompt = f"Develop a list of characters for a murder mystery game with the theme '{theme}'. Provide diverse personalities, backgrounds, and connections to the victim, including potential motives for each character."
    response = generate_response(prompt)
    return jsonify({'characters': response})


@app.route('/character-sheets', methods=['POST'])
def character_sheets():
    theme = request.json.get('theme')
    prompt = f"Generate character sheets for a murder mystery game with the theme '{theme}'. For each character, include a backstory, personality traits, relationships, and any public knowledge or rumors."
    response = generate_response(prompt)
    return jsonify({'character_sheets': response})


@app.route('/secret-information', methods=['POST'])
def secret_information():
    theme = request.json.get('theme')
    prompt = f"Create secret information for each character in a murder mystery game with the theme '{theme}'. Divide this information into three acts, ensuring each piece of information adds depth to the mystery and character motives."
    response = generate_response(prompt)
    return jsonify({'secret_information': response})


@app.route('/hosts-guide', methods=['POST'])
def hosts_guide():
    theme = request.json.get('theme')
    prompt = f"Compile a detailed master guide for the host of a murder mystery game with the theme '{theme}'. Include a plot summary, the real sequence of events of the murder, hidden clues, and tips for guiding the game."
    response = generate_response(prompt)
    return jsonify({'hosts_guide': response})


@app.route('/introduction-setup', methods=['POST'])
def introduction_setup():
    theme = request.json.get('theme')
    prompt = f"Write an introduction script for the host of a murder mystery game with the theme '{theme}'. This should set the scene, introduce characters, and explain the basic premise and rules of the game."
    response = generate_response(prompt)
    return jsonify({'introduction_setup': response})


@app.route('/clue-design', methods=['POST'])
def clue_design():
    theme = request.json.get('theme')
    prompt = f"Design a series of clues for a murder mystery game with the theme '{theme}'. Describe each clue, how it can be discovered, and its relevance to the mystery."
    response = generate_response(prompt)
    return jsonify({'clue_design': response})


@app.route('/costume-prop-suggestions', methods=['POST'])
def costume_prop_suggestions():
    theme = request.json.get('theme')
    prompt = f"Provide costume and prop suggestions for each character in a murder mystery game with the theme '{theme}', enhancing the game's immersion and thematic feel."
    response = generate_response(prompt)
    return jsonify({'costume_prop_suggestions': response})


@app.route('/game-flow-timing', methods=['POST'])
def game_flow_timing():
    theme = request.json.get('theme')
    prompt = f"Plan the timing and flow for a murder mystery game with the theme '{theme}'. Include the duration of each act, key events, and transitions."
    response = generate_response(prompt)
    return jsonify({'game_flow_timing': response})


@app.route('/resolution-reveal', methods=['POST'])
def resolution_reveal():
    theme = request.json.get('theme')
    prompt = f"Outline the resolution for a murder mystery game with the theme '{theme}'. Explain how the murderer is revealed, their method, and how this ties into the overall story."
    response = generate_response(prompt)
    return jsonify({'resolution_reveal': response})


@app.route('/debrief-discussion', methods=['POST'])
def debrief_discussion():
    theme = request.json.get('theme')
    prompt = f"Create a debrief structure for after a murder mystery game with the theme '{theme}'. Include points for discussion about player strategies, experiences, and the unraveling of the mystery."
    response = generate_response(prompt)
    return jsonify({'debrief_discussion': response})


@app.route('/feedback-mechanism', methods=['POST'])
def feedback_mechanism():
    theme = request.json.get('theme')
    prompt = f"Develop a feedback form for players to complete after participating in a murder mystery game with the theme '{theme}', focusing on areas of enjoyment and improvement."
    response = generate_response(prompt)
    return jsonify({'feedback_mechanism': response})


@app.route('/adaptation-group-size', methods=['POST'])
def adaptation_group_size():
    theme = request.json.get('theme')
    prompt = f"Provide strategies for adapting a murder mystery game with the theme '{theme}' for different group sizes, including modifications for character roles and plot elements."
    response = generate_response(prompt)
    return jsonify({'adaptation_group_size': response})


@app.route('/safety-comfort-guidelines', methods=['POST'])
def safety_comfort_guidelines():
    theme = request.json.get('theme')
    prompt = f"Draft guidelines to ensure safety, comfort, and respectful participation for players in a murder mystery game with the theme '{theme}', addressing potential sensitive topics and group dynamics."
    response = generate_response(prompt)
    return jsonify({'safety_comfort_guidelines': response})


if __name__ == '__main__':
    app.run(debug=True)
