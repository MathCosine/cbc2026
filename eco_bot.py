from cambc import *
from utils import get_closest_position, get_direction_to_core, smart_move

def run_eco_bot(c: Controller, core_pos: Position):
    if c.get_move_cooldown() > 0 and c.get_action_cooldown() > 0:
        return

    my_pos = c.get_position()
    titanium, axionite = c.get_global_resources()

    nearby_buildings = c.get_nearby_buildings(dist_sq=2)
    for b_id in nearby_buildings:
        b_type = c.get_entity_type(b_id)
        if b_type in (EntityType.HARVESTER, EntityType.FOUNDRY):
            if c.get_action_cooldown() == 0 and c.is_tile_empty(my_pos):
                dir_to_core = get_direction_to_core(c, my_pos, core_pos)
                if c.can_build_conveyor(my_pos, dir_to_core) and titanium > c.get_conveyor_cost()[0]:
                    c.build_conveyor(my_pos, dir_to_core)
                    return

    for b_id in nearby_buildings:
        if c.get_entity_type(b_id) == EntityType.HARVESTER:
            harvester_pos = c.get_position(b_id)
            if c.get_tile_env(harvester_pos) == Environment.ORE_AXIONITE:
                if c.get_action_cooldown() == 0 and c.is_tile_empty(my_pos):
                    if c.can_build_foundry(my_pos) and titanium > c.get_foundry_cost()[0]:
                        c.build_foundry(my_pos)
                        return

    target_env = Environment.ORE_AXIONITE if titanium > 300 else Environment.ORE_TITANIUM
    nearby_tiles = c.get_nearby_tiles()
    ore_tiles = [t for t in nearby_tiles if c.get_tile_env(t) == target_env]
    target_ore = get_closest_position(my_pos, ore_tiles)

    if target_ore:
        dist = my_pos.distance_squared(target_ore)
        if dist <= 2 and c.get_action_cooldown() == 0:
            if c.is_tile_empty(target_ore) and c.can_build_harvester(target_ore):
                if titanium > c.get_harvester_cost()[0]:
                    c.build_harvester(target_ore)
                    return
        elif dist > 2 and c.get_move_cooldown() == 0:
            smart_move(c, my_pos, target_ore)
            return

    if c.get_move_cooldown() == 0:
        # Create a target position directly away from the core
        outward_target = my_pos.add(core_pos.direction_to(my_pos))
        smart_move(c, my_pos, outward_target)
