from mesa import Agent
from sklearn import neighbors
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
        self.random_move()

    def eat_grass(self):
        """Eat grass."""
        # ... to be completed


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        # ... to be completed

    def try_eat(self):
        """Eat a sheep."""
        # get neighbors list
        neighbors_pos = self.model.grid.get_neighborhood(
            self.pos, moore=self.moore, include_center=True)
        # check if there is a sheep in the list
        neighbors = self.model.grid.get_cell_list_contents(neighbors_pos)
        sheeps_pos = list(filter(lambda x: isinstance(x, Sheep), neighbors))


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
        # ... to be completed

    def step(self):
        pass
        # ... to be completed
