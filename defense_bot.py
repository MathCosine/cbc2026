from cambc import *
from utils import smart_move

def run_defense_bot(c: Controller, core_pos: Position):
    my_pos = c.get_position()
    dist_from_core = my_pos.distance_squared(core_pos)
    titanium, _ = c.get_global_resources()

    if dist_from_core > 20 and c.get_action_cooldown() == 0:
        outward_dir = core_pos.direction_to(my_pos)
        if c.is_tile_empty(my_pos) and c.can_build_gunner(my_pos, outward_dir):
            if titanium > c.get_gunner_cost()[0] + 50:
                c.build_gunner(my_pos, outward_dir)
                return

    if c.get_move_cooldown() == 0:
        # Create a target position directly away from the core
        outward_target = my_pos.add(core_pos.direction_to(my_pos))
        smart_move(c, my_pos, outward_target)
