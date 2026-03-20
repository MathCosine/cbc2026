from cambc import *

def run_attack_bot(c: Controller, core_pos: Position):
    my_pos = c.get_position()
    my_team = c.get_team()
    titanium, _ = c.get_global_resources()

    if c.get_hp() <= 10:
        nearby = c.get_nearby_units(dist_sq=2)
        for uid in nearby:
            if c.get_team(uid) != my_team:
                c.self_destruct() 
                return

    if c.get_move_cooldown() > 0:
        return

    dist_from_core = my_pos.distance_squared(core_pos)
    map_size_sq = (c.get_map_width() / 2) ** 2 + (c.get_map_height() / 2) ** 2
    
    if dist_from_core > map_size_sq and titanium > c.get_gunner_cost()[0] + 50:
        if c.get_action_cooldown() == 0:
            outward_dir = core_pos.direction_to(my_pos)
            if c.is_tile_empty(my_pos) and c.can_build_gunner(my_pos, outward_dir):
                c.build_gunner(my_pos, outward_dir)
                return

    march_dir = core_pos.direction_to(my_pos)
    if not c.can_move(march_dir):
        march_dir = march_dir.rotate_right() 
        
    if c.can_move(march_dir):
        c.move(march_dir)
