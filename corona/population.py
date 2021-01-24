from enum import Enum
from random import random, randint, sample
from numpy.random import poisson


class Status(Enum):
    """Status enum class."""
    NotInfected = 0
    Infected = 1
    Recovered = 2


class Person:
    """Person class.

    Contains personal status and behaviour elements."""

    deniers_ratio = 0.25
    """The ratio of Corona deniers."""

    def __init__(self):
        """Initializer.

        Randomly assigns who is a denier and who isn't."""
        self.household = None

        self.knows_infected = False
        self.status = Status.NotInfected
        self.incubation = 0
        self.time_to_recover = 0

        self.is_denier = (random() < self.deniers_ratio)

    def infected(self):
        """Getter for whether the person is infected or not.

        :returns: the infection status of the person"""
        return self.status == Status.Infected

    def leaves_house(self):
        """Getter for whether or not the person might go outside.

        Only people who know they are infected and are not deniers will leave
        the house."""
        if self.infected():
            return self.is_denier or not self.knows_infected
        return True

    def infect(self):
        """Infect this person.

        Randomly assigns incubation period and recovery time."""
        if self.status == Status.NotInfected:
            self.status = Status.Infected
            self.incubation = randint(2, 5)
            self.time_to_recover = randint(self.incubation + 2, 10)

    def be_tested(self):
        """Test this person.

        If this person is infected and his incubation time is over, he will know
        he is infected after this test."""
        if self.infected():
            if not self.incubation:
                self.knows_infected = True
        else:
            self.knows_infected = False

    def age(self):
        """Make this person a day older.

        His incubation time will pass and eventually, he will recover."""
        if self.infected():
            self.incubation = max(self.incubation - 1, 0)
            self.time_to_recover = max(self.time_to_recover - 1, 0)

            if self.time_to_recover == 0:
                self.status = Status.Recovered
                self.knows_infected = False


class Household:
    """Household class.

    Container for a household of people who interact with eachother on a daily
    basis."""

    def __init__(self, people):
        """Initializer.

        :param people: the people who belong to this household"""
        self.people = people
        for person in self.people:
            person.household = self


class Population:
    """Population class.

    Contains population-level information:
    - the people in the simulation
    - the households they belong to
    - the people who are infected (regardless of whether they know
      themselves)"""

    def __init__(self, size, exp_household_size, n_infected):
        """Initializer.

        Randomly infects the given amount of people.

        :param size: the size of the population
        :param exp_household_size: the typical household size
        :param n_infected: the initial amount of people who are infected"""
        self.people = [Person() for _ in range(size)]
        self.households = []

        self.construct_households(exp_household_size)
        for person in sample(self.people, n_infected):
            person.infect()

    def construct_households(self, exp_num_size):
        """Construct the households.

        Households are mutually exclusive (one cannot belong to two'
        simultaneously).

        :param exp_num_size: the typical size of the household"""
        n_assigned = 0
        while n_assigned < len(self.people):
            num_in_household = poisson(exp_num_size)

            start = n_assigned
            stop = min(n_assigned + num_in_household, len(self.people))

            self.households.append(Household(self.people[start:stop]))

            n_assigned = stop

    def get_infected(self):
        """Get the infected people.

        :returns: the infected people (including the ones who don't know)"""
        return [person for person in self.people if person.infected()]


__all__ = ['Status', 'Person', 'Household', 'Population']
