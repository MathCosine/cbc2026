from cambc import *
from core_logic import run_core
from eco_bot import run_eco_bot
from attack_bot import run_attack_bot
from defense_bot import run_defense_bot
from turret_logic import run_turret

class Player:
    def __init__(self):
        self.core_pos = None

    def run(self, c: Controller):
        try:
            entity_type = c.get_entity_type()

            if entity_type == EntityType.CORE:
                if self.core_pos is None:
                    self.core_pos = c.get_position()
                run_core(c)
                
            elif entity_type == EntityType.BUILDER_BOT:
                if self.core_pos is None:
                    return 

                bot_id = c.get_id()
                role_number = bot_id % 5  # Returns 0, 1, 2, 3, or 4

                if role_number < 3:
                    run_eco_bot(c, self.core_pos)      # 60% chance
                elif role_number == 3:
                    run_attack_bot(c, self.core_pos)   # 20% chance
                else:
                    run_defense_bot(c, self.core_pos)  # 20% chance

            elif entity_type in (EntityType.GUNNER, EntityType.SENTINEL, EntityType.BREACH):
                run_turret(c)

        except GameError:
            pass 
        except Exception as e:
            print(f"Error on unit {c.get_id()}: {e}")
