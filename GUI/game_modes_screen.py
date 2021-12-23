from GUI.button import Button
from GUI.clickable_component import ClickableComponent
from GUI.drop_down_menu import DropDownMenu
from GUI.sub_screen import SubScreen
from base_pong.colors import *
from game_modes.game_mode_selector import GameModeSelector


class GameModesScreen(SubScreen):
    pong_type_menu = DropDownMenu(
        "Pong Types", GameModeSelector.all_pong_types, white, blue, 15, GameModeSelector.all_pong_types.index(GameModeSelector.pong_type))
    player_menu = DropDownMenu(
        "Number Of Players", GameModeSelector.all_player_options, white, blue, 15, GameModeSelector.all_player_options.index(GameModeSelector.number_of_players))
    game_mode_menu = DropDownMenu(
        "Game Modes", GameModeSelector.all_game_modes, white, blue, 15, GameModeSelector.all_game_modes.index(GameModeSelector.game_mode))
    length_used_up = 0
    height_used_up = 0
    name = "Game Modes"

    def initiate(length_used_up, height_used_up):
        GameModesScreen.set_item_bounds(
            GameModesScreen.game_mode_menu, length_used_up, height_used_up, 0, 5, 30, 6)
        GameModesScreen.set_item_bounds(
            GameModesScreen.player_menu, length_used_up, height_used_up, 35, 5, 30, 6)
        GameModesScreen.set_item_bounds(
            GameModesScreen.pong_type_menu, length_used_up, height_used_up, 70, 5, 30, 6)
        GameModeSelector.pong_type = GameModesScreen.pong_type_menu.selected_item
        GameModeSelector.game_mode = GameModesScreen.game_mode_menu.selected_item

    def render():
        GameModesScreen.player_menu.run()
        GameModesScreen.game_mode_menu.run()

        # The user gets to choose between certain game modes or choose a specific Pong Type like "Gravity Pong"
        # The Pong Types should only be displayed if they want to pick a specific Pong Type
        if GameModesScreen.game_mode_menu.get_selected_item() == "Pick Pong Type":
            GameModesScreen.pong_type_menu.run()

    def run():
        GameModesScreen.render()
        GameModeSelector.game_mode = GameModesScreen.game_mode_menu.get_selected_item()

        if GameModesScreen.game_mode_menu.get_selected_item() == "Pick Pong Type":
            GameModeSelector.pong_type = GameModesScreen.pong_type_menu.get_selected_item()

        
