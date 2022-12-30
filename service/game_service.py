from dao.game_dao import GameDao
from dao.game_dao import PlayerDao
from dao.game_dao import VesselDao
from model.player import Player
from model.vessel import Vessel
from model.battlefield import Battlefield
from model.game import Game

class GameService:
    def __init__(self):
        self.game_dao = GameDao()

    def create_game(self, player_name: str, min_x: int, max_x: int, min_y: int, max_y: int, min_z: int, max_z: int) -> int:
        game = Game()
        battle_field = Battlefield(min_x, max_x, min_y, max_y, min_z, max_z)
        game.add_player(Player(player_name, battle_field))
        return self.game_dao.create_game(game)

    def join_game(self, game_id: int, player_name: str) -> bool:
        game = self.game_dao.get_game(game_id)
        if game is None:
            # la partie n'existe pas
            return False
        if game.is_full():
            # la partie est déjà pleine
            return False
        # on ajoute le joueur à la partie
        game.add_player(Player(player_name, game.battlefield))
        self.game_dao.update_game(game)
        return True

    def get_game(self, game_id: int) -> Game:
        return self.game_dao.get_game(game_id)

    def add_vessel(self, game_id: int, player_name: str, vessel_type: str, x: int, y: int, z: int) -> bool:
        game = self.game_dao.get_game(game_id)
        if game is None:
            # la partie n'existe pas
            return False
        player = game.get_player(player_name)
        if player is None:
            # le joueur n'est pas dans la partie
            return False
        # on ajoute le vaisseau au joueur
        player.add_vessel(Vessel(vessel_type, x, y, z))
        self.game_dao.update_game(game)
        return True

    def shoot_at(self, game_id: int, shooter_name: str, vessel_id: int, x: int, y: int, z: int) -> bool:
        game = self.game_dao.get_game(game_id)
        if game is None:
            # la partie n'existe pas
            return False
        shooter = game.get_player(shooter_name)
        if shooter is None:
            # le tireur n'est pas dans la partie
            return False
        vessel = shooter.get_vessel(vessel_id)
        if vessel is None:
            # le tireur n'a pas de vaisseau avec cet id
            return False
        # on tire sur la cible
        success = vessel.shoot_at(x, y, z)
        self.game_dao.update_game(game)
        return success

    def get_game_status(self, game_id: int, shooter_name: str) -> str:
        game = self.get_game()
        player = [p for p in game.get_players if p.name == shooter_name][0]
        battle_field = player.get_battlefield()
    
