"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_sheep=100,
        initial_wolves=50,
        initial_grass=200,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=False,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            initial_grass : Number of grass patches to start with
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.initial_grass = initial_grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
                "Grass": lambda m: m.schedule.get_breed_count(GrassPatch),
            }
        )

        # Create sheep:
        for sheep_id in range(initial_sheep):
            pos = self.get_random_pos()
            new_sheep = Sheep(sheep_id, pos, self, moore=True, energy=None)
            self.schedule.add(new_sheep)
            self.grid.place_agent(agent=new_sheep, pos=pos)

        for wolf_id in range(initial_wolves):
            pos = self.get_random_pos()
            new_wolf = Wolf(wolf_id, pos, self, moore=True, energy=None)
            self.schedule.add(new_wolf)
            self.grid.place_agent(agent=new_wolf, pos=pos)

        if grass:
            # Create grass patches
            for grass_id in range(initial_grass):
                pos = self.get_random_pos()
                new_grass_patch = GrassPatch(
                    grass_id, pos, self, fully_grown=True, countdown=self.grass_regrowth_time)
                self.schedule.add(new_grass_patch)
                self.grid.place_agent(agent=new_grass_patch, pos=pos)

    def step(self):
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

        # ... to be completed

    def run_model(self, step_count=200):
        # ... to be completed
        for _ in range(step_count):
            self.step()

    def get_random_pos(self):
        """get random pos."""
        return (
            self.random.randrange(self.grid.width),
            self.random.randrange(self.grid.height),
        )
