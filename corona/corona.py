from random import randrange, random, seed as rd_seed
from numpy.random import poisson, seed as np_seed

from population import Status, Population


class Evolution:
    """Evolution class.

    Creates a simulation with a given population size
    and some behaviour-related parameters."""

    def __init__(self, population, movement_ratio, contact_ratio,
                 infection_probability, test_ratio):
        """Initializer.

        :param population: the population to run the simulation on
        :param movement_ratio: how many times per day a person typically goes
                               outside
        :param contact_ratio: the amount of times someone has contact per time
                              he/she goes out
        :param infection_probability: the probability someone is infected
                                      at contact
        :param test_ratio: how often someone with symptoms is typically tested
                           per day"""
        self.population = population
        self.movement_ratio = movement_ratio
        self.contact_ratio = contact_ratio
        self.infection_probability = infection_probability
        self.test_ratio = test_ratio

    def get_n_infected(self):
        """Get the total amount of infected people at current timestep."""
        return len(self.population.get_infected())

    def total_cases(self):
        """Get the total amount of cases.

        Includes both active and recovered cases.

        :returns: the total amount of cases"""
        result = 0
        for person in self.population.people:
            if person.status != Status.NotInfected:
                result += 1
        return result

    def timestep(self):
        """Simulate a single day."""
        for person in self.population.people:
            person.age()

        self.go_outside()
        self.go_home()
        self.test()

    def have_contact(self, person_a, person_b):
        """Simulate contact between two people.

        :param person_a: the first person of the interaction
        :param person_b: the second person of the interaction"""
        if person_a.infected() and random() < self.infection_probability:
            person_b.infect()
        if person_b.infected() and random() < self.infection_probability:
            person_a.infect()

    def go_outside(self):
        """Simulate the time of the day when people go outside.

        First selects who goes outside, then creates contacts between the ones
        that do."""
        meeters = []
        for person in self.population.people:
            if person.leaves_house() \
                    and random() < self.movement_ratio:
                # person goes outside
                meeters.append(person)

        for person in meeters:
            n_contacts = poisson(self.contact_ratio)
            for _ in range(n_contacts):
                others = [p for p in meeters if p is not person]
                other_person = others[randrange(len(others))]
                self.have_contact(person, other_person)

    def go_home(self):
        """Simulates the point where everyone goes home.

        This simulates the fact that after people go outside, they also
        interact with their own household."""
        for household in self.population.households:
            for person in household.people:
                for other in household.people:
                    if other is not person:
                        self.have_contact(person, other)

    def test(self):
        """Simulates the testing of infected people."""
        for person in self.population.get_infected():
            if random() < self.test_ratio:
                person.be_tested()


class Runner:
    """Runner class."""

    def __init__(self, evolution):
        """Initializer.

        :param evolution: the infection evolution instance to run"""
        self.evolution = evolution
        self.infected_over_time = []

    def run(self, timesteps):
        """Run the simulation for a given number of days.

        Will break the simulation when there no infected patients anymore.
        Logs the total amount of people that were infected at the end of the
        run.

        :param timesteps: the amount of days to simulate"""
        for _ in range(timesteps):
            self.evolution.timestep()

            n_infected = self.evolution.get_n_infected()
            self.infected_over_time.append(n_infected)
            if n_infected == 0:
                break


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    rd_seed(707)
    np_seed(1337)

    totals = []
    plt.subplot(121)
    for _ in range(10):
        population = Population(size=1000, exp_household_size=2.3,
                                n_infected=2)
        evolution = Evolution(population=population,
                              movement_ratio=0.25, contact_ratio=1,
                              infection_probability=0.25, test_ratio=0.5)

        runner = Runner(evolution)
        runner.run(100)

        plt.plot(runner.infected_over_time)
        totals.append(evolution.total_cases())
        print('Total #cases:', evolution.total_cases())

    plt.title('Active cases over time\n(different scenarios)')
    plt.xlabel('time (days)')
    plt.ylabel('#active cases')

    plt.subplot(122)
    plt.hist(totals)
    plt.title('Histogram of total\ncases per scenario')
    plt.xlabel('Total #cases')
    plt.xlabel('#runs in bin')
    plt.show()
