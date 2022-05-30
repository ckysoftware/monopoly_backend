import uuid
from dataclasses import dataclass, field

import game

from host.localhost import LocalHost
from host.user import User

# from typing import Optional


# from game.actions import Action


@dataclass(kw_only=True, slots=True)
class Room:
    host: User
    name: str
    uid: str = field(default_factory=lambda: str(uuid.uuid4()))
    users: list[User] = field(default_factory=list)
    localhost: LocalHost = field(init=False)
    # NOTE MAYBE add user num limit

    def add_user(self, user: User) -> None:
        if user in self.users:
            raise ValueError(f"User '{user.uid}' already in room '{self.uid}'")
        self.users.append(user)

    def remove_user(self, user: User) -> None:
        self.users.remove(user)

    def start_localhost(self) -> None:
        self.localhost = LocalHost(users=self.users)
        dice_rolls = self.localhost.start_game()
        print(f"Dice rolls for deciding playing orders: {dice_rolls}")


@dataclass(kw_only=True, slots=True)
class server:
    # NOTE may be change this to server? host should be the interface
    """
    Server for monopoly game.
    """

    # TODO add user_uid check in public Host _get_user() -> return error
    # TODO add room_uid check in public Host _get_room() -> return error
    # TODO need establish connection to user
    # active_players: dict[str, Room] = field(default_factory=dict)  # user_uid, Room
    active_users: dict[str, User] = field(default_factory=dict)  # user_uid, User
    games: dict[str, game.Game] = field(default_factory=dict)  # game_uid, Game
    rooms: dict[str, Room] = field(default_factory=dict)  # room_uid, Room

    def add_user(self, name: str) -> User:
        new_user = User(name=name)
        self.active_users[new_user.uid] = new_user
        return new_user

    def create_room(self, user_uid: str, name: str) -> str:
        user = self.active_users[user_uid]
        if user.room_uid is not None:
            raise ValueError(f"User '{user_uid}' already in room '{user.room_uid}'")
        new_room = Room(host=user, name=name)
        self.rooms[new_room.uid] = new_room
        return new_room.uid

    def list_rooms(self):
        return [
            {
                "name": room.name,
                "host": room.host.name,
                "uid": room.uid,
            }
            for room in self.rooms.values()
        ]

    def join_room(self, user_uid: str, uid: str) -> None:
        user = self.active_users[user_uid]
        self.rooms[uid].add_user(user)
        user.room_uid = uid

    def leave_room(self, user_uid: str) -> None:
        user = self.active_users[user_uid]
        assert user.room_uid is not None
        self.rooms[user.room_uid].remove_user(user)
        user.room_uid = None

    # def create_game(self, room_uid: str) -> None:
    #     self.rooms[room_uid].create_game()

    # def delete_room(self, uid: str) -> None:
    #     self.rooms.pop(uid)

    # def add_player_token(self, user_uid: str, token: int) -> None:
    #     user = self.active_users[user_uid]
    #     assert user.room_uid is not None
    #     self.rooms[user.room_uid].assign_player_token(user=user, token=token)
