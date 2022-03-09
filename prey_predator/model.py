"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""
from typing import Union
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.random_walk import RandomWalker
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
        height=50,
        width=50,
        initial_sheep=100,
        initial_wolves=50,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        initial_wolf_enery=3,
        initial_sheep_energy=10,
        wolf_gain_from_food=20,
        grass=True,
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
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.initial_wolf_enery = initial_wolf_enery
        self.initial_sheep_energy = initial_sheep_energy

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
        self.unique_id = 0
        for _ in range(initial_sheep):
            pos = self.get_random_pos()
            new_sheep = Sheep(
                self.unique_id, pos, self, moore=True, energy=self.initial_sheep_energy
            )
            self.schedule.add(new_sheep)
            self.grid.place_agent(agent=new_sheep, pos=pos)
            self.unique_id += 1

        for _ in range(initial_wolves):
            pos = self.get_random_pos()
            new_wolf = Wolf(
                self.unique_id, pos, self, moore=True, energy=self.initial_wolf_enery
            )
            self.schedule.add(new_wolf)
            self.grid.place_agent(agent=new_wolf, pos=pos)
            self.unique_id += 1

        if grass:
            # Create grass patches
            for x in range(width):
                for y in range(height):
                    pos = (x, y)
                    new_grass_patch = GrassPatch(
                        self.unique_id,
                        pos,
                        self,
                        fully_grown=True,
                        countdown=self.grass_regrowth_time,
                    )
                    self.schedule.add(new_grass_patch)
                    self.grid.place_agent(agent=new_grass_patch, pos=pos)
                    self.unique_id += 1

    def step(self):
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

        # ... to be completed

    # pylint: disable=arguments-differ
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

    def kill_agent(self, agent: Agent):
        """Kill one agent."""
        self.schedule.remove(agent)
        self.grid.remove_agent(agent)

    def wolf_eat_sheep(self, wolf: Wolf, sheep: Sheep):
        """Wolf eat one sheep."""
        self.kill_agent(sheep)
        wolf.energy += self.wolf_gain_from_food

    def sheep_eat_grass(self, sheep: Sheep, grass: GrassPatch):
        """Sheep eat one grass patch."""
        grass.alive = False
        grass.countdown = grass.max_countdown
        if sheep.energy is not None:
            sheep.energy = sheep.energy + self.sheep_gain_from_food

    def reproduce_wolf(self, agent: Union[Sheep, Wolf]):
        """Reproduce wolf."""
        if self.random.random() < self.wolf_reproduce:
            pos = agent.pos
            new_agent = Wolf(
                self.unique_id, pos, self, moore=True, energy=self.initial_wolf_enery
            )
            self.schedule.add(new_agent)
            self.grid.place_agent(agent=new_agent, pos=pos)
            self.unique_id += 1

    def reproduce_sheep(self, agent: Union[Sheep, Wolf]):
        """Reproduce sheep."""
        if self.random.random() < self.sheep_reproduce:
            pos = agent.pos or self.get_random_pos()
            new_agent = Sheep(
                self.unique_id, pos, self, moore=True, energy=self.initial_sheep_energy
            )
            self.schedule.add(new_agent)
            self.grid.place_agent(agent=new_agent, pos=pos)
            self.unique_id += 1
