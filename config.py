# Importing modules
import json


# Getting data from JSON
data = json.load(open('config.json'))

# Variables for bot
api_token = data['api_token']
main_menu_buttons = data['main_menu_buttons']
novels = data['novels']
contacts = data['contacts']
info = data['info']
helpList = data['helpList']
hello = data['hello']

# Callback lists
novels_callback_id = [str(i) for i in range(len(novels))]
about_callback_id = [f'about {str(i)}' for i in range(len(novels_callback_id))]
characters_callback_id = [f'characters {str(i)}' for i in range(len(novels_callback_id))]


