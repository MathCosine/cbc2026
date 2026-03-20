from cambc import *

def get_target_priority(c: Controller, entity_id: int) -> int:
    ent_type = c.get_entity_type(entity_id)
    if ent_type == EntityType.CORE:
        return 4
    if ent_type in (EntityType.BREACH, EntityType.SENTINEL, EntityType.GUNNER, EntityType.LAUNCHER):
        return 3
    if ent_type == EntityType.BUILDER_BOT:
        return 2
    return 1 

def run_turret(c: Controller):
    if c.get_action_cooldown() > 0 or c.get_ammo_amount() == 0:
        return

    my_team = c.get_team()
    nearby_units = c.get_nearby_units()
    
    best_target_pos = None
    highest_priority = -1

    for unit_id in nearby_units:
        if c.get_team(unit_id) != my_team:
            enemy_pos = c.get_position(unit_id)
            if c.can_fire(enemy_pos):
                priority = get_target_priority(c, unit_id)
                if priority > highest_priority:
                    highest_priority = priority
                    best_target_pos = enemy_pos

    if best_target_pos:
        c.fire(best_target_pos)
