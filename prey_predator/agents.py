from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        # Move
        self.random_move()
        if self.energy is not None:
            self.energy -= 1
        
        # Eat grass
        self.eat_grass()

        # Die
        if self.energy is not None and self.energy <=0:
            self.model.kill_agent(self)

        # Reproduce
        self.model.reproduce_sheep(self)


    def eat_grass(self):
        """Eat grass."""
        neighbors = self.model.grid.get_cell_list_contents(self.pos)
        grass_below = list(filter(lambda x: isinstance(x, GrassPatch) and x.alive, neighbors))
        if len(grass_below) > 0:
            to_eat = self.random.choice(grass_below)
            self.model.sheep_eat_grass(self, to_eat)


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """


    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """Step for the wolf.
        1- Move
        2- Try to eat a sheep
        3- Die if no energy
        4- Reproduction
        """
        # Move
        self.random_move()
        self.energy -= 1

        # Eat
        self.try_eat()

        # If no more energy
        if self.energy <= 0:
            self.model.kill_agent(self)
            return

        # Reproduction
        self.model.reproduce_wolf(self)

    def try_eat(self):
        """Eat a sheep."""
        # get neighbors list
        neighbors_pos = self.model.grid.get_neighborhood(
            self.pos, moore=self.moore, include_center=True
        )
        # check if there is a sheep in the list
        neighbors = self.model.grid.get_cell_list_contents(neighbors_pos)
        sheeps = list(filter(lambda x: isinstance(x, Sheep), neighbors))
        if len(sheeps) > 0:
            to_kill = self.random.choice(sheeps)
            self.model.wolf_eat_sheep(self, to_kill)


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.alive = fully_grown
        self.max_countdown = countdown
        self.countdown = -1


    def step(self):
        if not self.alive:
            if self.countdown <= 0:
                self.alive = True
            self.countdown -= 1

