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
