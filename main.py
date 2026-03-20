from cambc import *
from core_logic import run_core
from eco_bot import run_eco_bot
from attack_bot import run_attack_bot
from defense_bot import run_defense_bot
from turret_logic import run_turret

class Player:
    def __init__(self):
        # Every unit gets its own copy of this variable
        self.core_pos = None

    def run(self, c: Controller):
        try:
            entity_type = c.get_entity_type()

            if entity_type == EntityType.CORE:
                if self.core_pos is None:
                    self.core_pos = c.get_position()
                run_core(c)
                
            elif entity_type == EntityType.BUILDER_BOT:
                # If we don't know where the core is, look around!
                if self.core_pos is None:
                    my_team = c.get_team()
                    nearby_buildings = c.get_nearby_buildings()
                    
                    for b_id in nearby_buildings:
                        if c.get_entity_type(b_id) == EntityType.CORE and c.get_team(b_id) == my_team:
                            self.core_pos = c.get_position(b_id)
                            break
                            
                # If we STILL don't know (which shouldn't happen), skip turn
                if self.core_pos is None:
                    return 

                # Now that we know where home is, assign roles and get to work
                bot_id = c.get_id()
                role_number = bot_id % 5  

                if role_number < 3:
                    run_eco_bot(c, self.core_pos)      
                elif role_number == 3:
                    run_attack_bot(c, self.core_pos)   
                else:
                    run_defense_bot(c, self.core_pos)  

            elif entity_type in (EntityType.GUNNER, EntityType.SENTINEL, EntityType.BREACH):
                run_turret(c)

        except GameError:
            # We catch game errors so the bot doesn't crash if it tries an illegal move
            pass 
        except Exception as e:
            print(f"Error on unit {c.get_id()}: {e}")
