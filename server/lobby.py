from games.game import Game
from server_message_queue import server_q_put

class Lobby:
    def __init__(self, client_conn, client_count, game_type, client_id):
        self.id = client_id
        self.clients = [
            {
                'conn': client_conn,
                'role': 'HOST',
                'id': 0,
                'turn': 1,
                'end_game': False
                #name: name TODO: add name
                #points: 0 TODO: add points from game (maybe in self.game is better)
            }
        ]
        self.host = self.clients[0]
        self.client_count = client_count
        self.game_type = game_type
        self.game = Game(game_type)
        self.game.add_client(client_conn)
        self.ready = False
        self.clients_times = self.game.clients_times
        self.clients_status = self.game.clients_status
        self.clients_limit = self.game.clients_limit
        self.closed = False
        self.active_turn = 0

    def add_client(self, client_conn, role, turn):
        self.client_count += 1
        self.clients.append(
            {
                'conn': client_conn,
                'role': role,
                'id': len(self.clients),
                'turn': turn,
                'end_game': False
            }
        )
        self.game.add_client(client_conn)

    def remove_client(self, client):
        client -= 1
        self.client_count -= 1
        try:
            self.clients[client] = 0
            self.game.remove_client(client)
            server_q_put('Removed client_del:', client)
        except IndexError:
            server_q_put('Client at:', client, 'is already deleted!')
