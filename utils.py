from cambc import *

def get_closest_position(target: Position, positions: list[Position]) -> Position | None:
    if not positions:
        return None
    closest = positions[0]
    min_dist = target.distance_squared(closest)
    for pos in positions[1:]:
        dist = target.distance_squared(pos)
        if dist < min_dist:
            min_dist = dist
            closest = pos
    return closest

def is_safe_to_move(c: Controller, pos: Position) -> bool:
    if not (0 <= pos.x < c.get_map_width() and 0 <= pos.y < c.get_map_height()):
        return False
    return c.is_tile_passable(pos) and c.get_tile_builder_bot_id(pos) is None

def get_direction_to_core(c: Controller, current_pos: Position, core_pos: Position) -> Direction:
    return current_pos.direction_to(core_pos)

def get_enemy_core_guesses(core_pos: Position, map_width: int, map_height: int) -> list[Position]:
    x, y = core_pos.x, core_pos.y
    return [
        Position(map_width - 1 - x, y),                 
        Position(x, map_height - 1 - y),                
        Position(map_width - 1 - x, map_height - 1 - y) 
    ]

def smart_move(c: Controller, current_pos: Position, target_pos: Position) -> bool:
    if c.get_move_cooldown() > 0:
        return False

    ideal_dir = current_pos.direction_to(target_pos)

    # Try direct
    if c.can_move(ideal_dir):
        c.move(ideal_dir)
        return True

    # Try sliding 45 degrees
    left_dir = ideal_dir.rotate_left()
    right_dir = ideal_dir.rotate_right()

    dist_left = current_pos.add(left_dir).distance_squared(target_pos)
    dist_right = current_pos.add(right_dir).distance_squared(target_pos)

    if dist_left <= dist_right and c.can_move(left_dir):
        c.move(left_dir)
        return True
    elif c.can_move(right_dir):
        c.move(right_dir)
        return True
    elif c.can_move(left_dir): 
        c.move(left_dir)
        return True

    return False
