from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:////tmp/tdlog.db', echo=True, future=True)
Base = declarative_base(bind=engine)


class GameEntity(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    players = relationship("PlayerEntity", back_populates="game",
    cascade="all, delete-orphan")

class PlayerEntity(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    game = relationship("GameEntity", back_populates="players")
    battle_field = relationship("BattlefieldEntity",
    back_populates="player",
    uselist=False, cascade="all, delete-orphan")

class BattlefieldEntity(Base):
    __tablename__ = 'battlefield'
    id = Column(Integer,primary_key = True)
    min_x = Column(Integer)
    min_y = Column(Integer)
    min_z = Column(Integer)
    max_x = Column(Integer)
    max_y = Column(Integer)
    max_z = Column(Integer)
    player_id = Column(Integer,ForeignKey("Player.id"),nullable=False)
    player = relationship("PlayerEntity", back_populates="battle_field",uselist = True,cascade="all, delete-orphan")
    vessels = relationship("VesselEntity", back_populates="battle",cascade="all, delete-orphan")

class VesselEntity(Base):
    __tablename__ = 'vessel'
    id = Column(Integer,primary_key = True)
    coord_x = Column(Integer)
    coord_y = Column(Integer)
    coord_z = Column(Integer)
    hits_to_be_destroyed = Column(Integer)
    Type = Column(String)
    battle_fiel_id = Column(Integer ,ForeignKey("Battlefield.id"),nullable=False)
    battle= relationship("BattlefieldEntity", back_populates = "vessel")
    weapon = relationship('WeapenEntity',c ,uselist = True, cascade="all, delete-orphan") 

class WeaponEntity(Base):
    __tablename__ = 'weapen'
    id = Column(Integer,primary_key = True)
    ammunitation = Column(Integer)
    Range = Column(Integer)
    Type = Column(String)
    vissel_id = Column(Integer,ForeignKey("vissel.id"),back_populates ="weapon")
    vessel = relationship("VesselEntity", back_populates = "weapen")

class VesselTypes:
    CRUISER = "Cruiser"
    DESTROYER = "Destroyer"
    FRIGATE = "Frigate"
    SUBMARINE = "Submarine"
class WeapenTypes : 
    AIRMISSILELAUNCHER = "AirMissileLauncher"
    SURFACEMISSILELAUNCHER = "SurfaceMissileLauncher"
    TORPEDOLAUNCHER = "TorpedoLauncher"



def map_to_game(game_entity : GameEntity):
    if game_entity is None:
        return None
    game = Game()
    game_id = game_entity.id
    for player_entity in game_entity.players:
        battle_field = Battlefield(player_entity.battle_field.min_x,
                                   player_entity.battle_field.max_x,
                                   player_entity.battle_field.min_y,
                                   player_entity.battle_field.max_y,
                                   player_entity.battle_field.min_z,
                                   player_entity.battle_field.max_z,
                                   player_entity.battle_field.max_power)

        battle_field.id = player_entity.battle_fiel_id
        battle_field.vessels = map_to_vessels(player_entity.battle_field.vessels)
        player.id = player_entity.id
        game.add_player(player)
    return game 

def map_to_vessels(vessel_entities : list([VesselEntity])):
    vessels : list[Vessel] = []
    for vessel_entity in vessel_entities: 
        weapon = map_to_weapon(vessel_entity.weapon)
        vessel = map_to_vessel(vessel_entity, weapon )
        vessels.append(vessel)
    return vessels

def map_to_vessel(vessel_entity,weapen) -> Optional[Vessel]:

    vessel = None
    if vessel_entity.type == VesselTypes.CRUISER:
        vessel = Cruiser(vessel_entity.coord_x,vessel_entity.coord_y,
            vessel_entity.coord_z)
        vessel.hits_to_be_destroyed = vessel_entity.hits_to_be_destroyed
        vessel.id = vessel_entity.id
        vessel.weapon = weapon 
        return vessel
    elif vessel_entity.type == VesselTypes.DESTROYER:
        vessel = Destroyer(vessel_entity.coord_x,vessel_entity.coord_y,
            vessel_entity.coord_z) 
        vessel.hits_to_be_destroyed = vessel_entity.hits_to_be_destroyed
        vessel.id = vessel_entity.id
        vessel.weapon = weapon
        return vessel
    elif vessel_entity.type ==VesselTypes.FRIGATE:
        vessel = Frigate(vessel_entity.coord_x,vessel_entity.coord_y,
            vessel_entity.coord_z) 
        vessel.hits_to_be_destroyed = vessel_entity.hits_to_be_destroyed
        vessel.id = vessel_entity.id
        vesel.weapon = weapon
        return vessel
    elif vessel_entity.type ==VesselTypes.SUBMARINE:
        vessel = Submarine(vessel_entity.coord_x,vessel_entity.coord_y,
            vessel_entity.coord_z) 
        vessel.hits_to_be_destroyed = vessel_entity.hits_to_be_destroyed
        vessel.id = vessel_entity.id
        vessel.weapon = weapon
        return vessel 
    return vessel          

def map_to_weapon(weapon_entity : WeaponEntity) -> Optional[Weapon]:
    weapon = None
    if weapon_entity.type == WeaponTypes.SURFACEMISSILELELAUNCHER:
        weapon = SurfaceMissileLauncher()
        weapon.id = weapon_entity.id
        weapon.range = weapon_entity.range
        weapon.ammunitions = weapon_entity.ammunitions
        return weapon
    elif weapon_entity.type == WeaponTypes.TORPEDOLAUNCHER:
        weapon = TorpedoLauncher()
        weapon.id = weapon_entity.id
        weapon.range = weapon_entity.range
        weapon.ammunitions = weapon_entity.ammunitions 
        return weapon
    
    elif weapon_entity.type ==WeaponTypes.AIRMISSILELAUNCHER:
        weapon = AirMissileLauncher()
        weapon.id = weapon_entity.id
        weapon.range = weapon_entity.range
        weapon.ammunitions = weapon_entity.ammunitions 
        return weapon
    return weapon



class GameDao:
    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session()

    def create_game(self, game: Game) -> int:
        game_entity = map_to_game_entity(game)
        self.db_session.add(game_entity)
        self.db_session.commit()
        return game_entity.id

    def find_game(self, game_id: int) -> Game:
        stmt = select(GameEntity).where(GameEntity.id == game_id)
        game_entity = self.db_session.scalars(stmt).one()
        return map_to_game(game_entity)

    def create_or_update_player(self,game_id : int, player: Player ) -> bool:
        stmt = select(GameEntity).where(GameEntity.id == game_id)
        game_entity = self.db_session.scalars(stmt).one()
        for player_entity in game_entity.players:
            if player_entity.name == player.name:
                game_entity.players.remove(player_entity)
                break
        game_entity.players.append(map_to_player_entity(player))
        self.db_session.flush()
        self.db_session.commit()
        return True 

    
    def create_or_update_vessel(self,player : Player,vessel : Vessel) -> bool:
        stmt_find_player = select(PlayerEntity).where(PlayerEntity.id == player.id)
        player_entity= self.db_session.scalars(stmt_find_player).one()
        vessel_entity_updated = map_to_vessel_entity(player.get_battlefield().id,vessel)
        for vessel_entity in player_entity.battle_field.vessels:
            if vessel_entity.id == vessel_entity_updated.id:
                player_entity.battle_field.vessels.remove(vessel_entity)
                break
        player_entity.battle_field.vessels.append(vessel_entity_updated)
        self.db_session.flush()
        self.db_session.commit()
        return True



    


    




    






