from cambc import *
from utils import get_enemy_core_guesses, smart_move

def run_attack_bot(c: Controller, core_pos: Position):
    my_pos = c.get_position()
    my_team = c.get_team()
    
    # 1. Survival Check
    if c.get_hp() <= 10:
        nearby = c.get_nearby_units(dist_sq=2)
        for uid in nearby:
            if c.get_team(uid) != my_team:
                c.self_destruct() 
                return
    
    if c.get_move_cooldown() > 0:
        return

    # 2. The Marker Network (Swarm Logic)
    nearby_entities = c.get_nearby_entities(dist_sq=c.get_vision_radius_sq())
    swarm_target = None
    
    for uid in nearby_entities:
        if c.get_entity_type(uid) == EntityType.CORE and c.get_team(uid) != my_team:
            if c.can_place_marker(my_pos):
                c.place_marker(my_pos, 999)
            swarm_target = c.get_position(uid)
            break
            
        elif c.get_entity_type(uid) == EntityType.MARKER and c.get_team(uid) == my_team:
            if c.get_marker_value(uid) == 999:
                swarm_target = c.get_position(uid)

    if swarm_target:
        smart_move(c, my_pos, swarm_target)
        return

    # 3. Exploration (Symmetry Guessing)
    guesses = get_enemy_core_guesses(core_pos, c.get_map_width(), c.get_map_height())
    my_guess = guesses[c.get_id() % 3] 
    
    smart_move(c, my_pos, my_guess)
