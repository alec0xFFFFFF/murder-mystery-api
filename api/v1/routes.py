from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid
import pystache
from flask import Blueprint, request, jsonify

from agents import baseAgent

bp = Blueprint('bp', __name__)


def render_template(file_name, context):
    with open(file_name, 'r') as file:
        template = file.read()
    return pystache.render(template, context)


games = {}  # Store game data


# Endpoint to create a new game
@bp.route('/create-game', methods=['POST'])
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
@bp.route('/advance-game', methods=['POST'])
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
@bp.route('/narrate-storyline', methods=['POST'])
def narrate_storyline():
    game_id = request.json.get('game_id')
    act = request.json.get('act')

    if game_id in games:
        storyline = get_storyline_for_act(game_id, act)  # Implement this function based on your game logic
        agent = baseAgent.Agent()
        audio_url = agent.generate_audio(storyline)
        return jsonify({'audio_url': audio_url})
    else:
        return jsonify({'error': 'Game not found'}), 404


@bp.route('/theme-selection', methods=['POST'])
def theme_selection():
    theme = request.json.get('theme')
    prompt = render_template('prompts/theme_selection.prompt', {'theme': theme})
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'details': response})


@bp.route('/setting-time-period', methods=['POST'])
def setting_time_period():
    theme = request.json.get('theme')
    prompt = f"Describe the setting and time period for a murder mystery game based on the theme '{theme}'. Include details about the environment, cultural context, and historical elements relevant to this theme."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'setting_time_period': response})


@bp.route('/main-plot-outline', methods=['POST'])
def main_plot_outline():
    theme = request.json.get('theme')
    prompt = f"Create a basic plot outline for a murder mystery game with the theme '{theme}'. Detail the central event, the reason for the gathering, and the victim's role in the story."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'plot_outline': response})


@bp.route('/character-creation', methods=['POST'])
def character_creation():
    theme = request.json.get('theme')
    prompt = f"Develop a list of characters for a murder mystery game with the theme '{theme}'. Provide diverse personalities, backgrounds, and connections to the victim, including potential motives for each character."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'characters': response})


@bp.route('/character-sheets', methods=['POST'])
def character_sheets():
    theme = request.json.get('theme')
    prompt = f"Generate character sheets for a murder mystery game with the theme '{theme}'. For each character, include a backstory, personality traits, relationships, and any public knowledge or rumors."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'character_sheets': response})


@bp.route('/secret-information', methods=['POST'])
def secret_information():
    theme = request.json.get('theme')
    prompt = f"Create secret information for each character in a murder mystery game with the theme '{theme}'. Divide this information into three acts, ensuring each piece of information adds depth to the mystery and character motives."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'secret_information': response})


@bp.route('/hosts-guide', methods=['POST'])
def hosts_guide():
    theme = request.json.get('theme')
    prompt = f"Compile a detailed master guide for the host of a murder mystery game with the theme '{theme}'. Include a plot summary, the real sequence of events of the murder, hidden clues, and tips for guiding the game."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'hosts_guide': response})


@bp.route('/introduction-setup', methods=['POST'])
def introduction_setup():
    theme = request.json.get('theme')
    prompt = f"Write an introduction script for the host of a murder mystery game with the theme '{theme}'. This should set the scene, introduce characters, and explain the basic premise and rules of the game."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'introduction_setup': response})


@bp.route('/clue-design', methods=['POST'])
def clue_design():
    theme = request.json.get('theme')
    prompt = f"Design a series of clues for a murder mystery game with the theme '{theme}'. Describe each clue, how it can be discovered, and its relevance to the mystery."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'clue_design': response})


@bp.route('/costume-prop-suggestions', methods=['POST'])
def costume_prop_suggestions():
    theme = request.json.get('theme')
    prompt = f"Provide costume and prop suggestions for each character in a murder mystery game with the theme '{theme}', enhancing the game's immersion and thematic feel."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'costume_prop_suggestions': response})


@bp.route('/game-flow-timing', methods=['POST'])
def game_flow_timing():
    theme = request.json.get('theme')
    prompt = f"Plan the timing and flow for a murder mystery game with the theme '{theme}'. Include the duration of each act, key events, and transitions."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'game_flow_timing': response})


@bp.route('/resolution-reveal', methods=['POST'])
def resolution_reveal():
    theme = request.json.get('theme')
    prompt = f"Outline the resolution for a murder mystery game with the theme '{theme}'. Explain how the murderer is revealed, their method, and how this ties into the overall story."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'resolution_reveal': response})


@bp.route('/debrief-discussion', methods=['POST'])
def debrief_discussion():
    theme = request.json.get('theme')
    prompt = f"Create a debrief structure for after a murder mystery game with the theme '{theme}'. Include points for discussion about player strategies, experiences, and the unraveling of the mystery."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'debrief_discussion': response})


@bp.route('/feedback-mechanism', methods=['POST'])
def feedback_mechanism():
    theme = request.json.get('theme')
    prompt = f"Develop a feedback form for players to complete after participating in a murder mystery game with the theme '{theme}', focusing on areas of enjoyment and improvement."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'feedback_mechanism': response})


@bp.route('/adaptation-group-size', methods=['POST'])
def adaptation_group_size():
    theme = request.json.get('theme')
    prompt = f"Provide strategies for adapting a murder mystery game with the theme '{theme}' for different group sizes, including modifications for character roles and plot elements."
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt)
    return jsonify({'adaptation_group_size': response})


@bp.route('/safety-comfort-guidelines', methods=['POST'])
def safety_comfort_guidelines():
    theme = request.json.get('theme')
    prompt = (f"Draft guidelines to ensure safety, comfort, and respectful participation for players in a murder "
              f"mystery game with the theme '{theme}', addressing potential sensitive topics and group dynamics.")
    agent = baseAgent.Agent()
    response = agent.generate_response(prompt, "")
    return jsonify({'safety_comfort_guidelines': response})


def init_api_v1(app):
    app.register_blueprint(bp, url_prefix='/v1')
