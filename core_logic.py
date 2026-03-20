from cambc import *
from utils import is_safe_to_move

def run_core(c: Controller):
    if c.get_action_cooldown() > 0:
        return

    titanium, axionite = c.get_global_resources()
    bot_cost = c.get_builder_bot_cost()[0]

    # Keep at least 100 Titanium in reserve
    if titanium > bot_cost + 100:
        my_pos = c.get_position()
        
        for direction in Direction:
            if direction == Direction.CENTRE:
                continue
            spawn_pos = my_pos.add(direction)
            if is_safe_to_move(c, spawn_pos) and c.can_spawn(spawn_pos):
                c.spawn_builder(spawn_pos)
                return
