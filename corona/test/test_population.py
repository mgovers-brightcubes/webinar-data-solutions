import pytest
from unittest.mock import patch

from random import seed, choice
from population import Status, Person, Household, Population


@pytest.fixture()
def obeyer():
    person_ = Person()
    person_.is_denier = False
    return person_


@pytest.fixture()
def denier():
    person_ = Person()
    person_.is_denier = True
    return person_


@pytest.fixture(params=[True, False])
def person(request):
    person_ = Person()
    person_.is_denier = request.param
    return person_


@pytest.fixture(params=[Status.NotInfected, Status.Infected,
                        Status.Recovered])
def status(request):
    return request.param


def test_person():
    seed(1337)
    expected_deniers = [False, False, False, False, True, False]
    for i in range(6):
        person = Person()
        assert person.status == Status.NotInfected
        assert not person.knows_infected
        assert person.incubation == 0
        assert person.time_to_recover == 0
        assert person.is_denier == expected_deniers[i]


def test_person_infected(person, status):
    person.status = status
    assert person.infected() == (status == Status.Infected)


@pytest.mark.parametrize("knows", [False, True])
def test_person_leaves_house(person, status, knows):
    person.status = status
    person.knows_infected = knows
    if status == Status.Infected and knows:
        assert person.leaves_house() == person.is_denier
    else:
        assert person.leaves_house() 


def test_person_infect(person, status):
    person.status = status
    original_incubation = person.incubation
    original_time_to_recover = person.incubation
    
    person.infect()
    if status == Status.Recovered:
        assert person.status == status
    else:
        assert person.status == Status.Infected
        if status == Status.NotInfected:
            assert person.incubation > 0
            assert person.time_to_recover > 0
        else:
            assert person.incubation == original_incubation
            assert person.time_to_recover == original_time_to_recover


@pytest.mark.parametrize("knows", [True, False])
@pytest.mark.parametrize("incubation", range(3))
def test_person_be_tested(person, status, knows, incubation):
    person.status = status
    person.knows_infected = knows
    person.incubation = incubation
    person.be_tested()
    if status == Status.Infected:
        if person.incubation:
            assert person.knows_infected == knows
        else:
            assert person.knows_infected
    else:
        assert not person.knows_infected


@pytest.mark.parametrize("incubation", range(3))
@pytest.mark.parametrize("recovery", range(3))
def test_person_age_incubation(person, status, incubation, recovery):
    person.status = status
    person.incubation = incubation
    person.time_to_recover = recovery
    person.age()

    if status == Status.Infected:
        assert person.incubation == max(0, incubation - 1)
        assert person.time_to_recover == max(0, recovery - 1)
        if person.time_to_recover == 0:
            assert person.status == Status.Recovered
        else:
            assert person.status == Status.Infected
    else:
        assert person.status == status
        assert person.incubation == incubation
        assert person.time_to_recover == recovery


def test_household():
    with patch('population.Person', spec=True) as p_a, \
            patch('population.Person', spec=True) as p_b:
        p_list = [p_a, p_b]
        household = Household(p_list)
        assert household.people == p_list
        assert p_a.household == household
        assert p_b.household == household


@pytest.mark.parametrize('size', [3, 10])
@pytest.mark.parametrize('exp_household_size', [1, 5])
@pytest.mark.parametrize('n_infected', [0, 3])
@patch.object(Population, 'construct_households')
def test_population(mock, size, exp_household_size, n_infected):
    population = Population(size, exp_household_size, n_infected)
    assert len(population.people) == size
    for p in population.people:
        assert isinstance(p, Person)
    
    assert population.households == []
    mock.assert_called_once_with(exp_household_size)

    infected = population.get_infected()
    assert infected == [p for p in population.people if p.infected()]
    assert len(infected) == n_infected


@pytest.mark.parametrize('exp_household_size', [1, 5])
def test_population_households(exp_household_size):
    population = Population(20, exp_household_size, 0)
    for p in population.people:
        assert p.household is not None
        assert p.household in population.households

        # unique
        assert len([household for household in population.households
                              if household == p.household]) == 1


@pytest.mark.parametrize('n_infected', [0, 1, 5])
def test_population_get_infected(n_infected):
    def verify_infected(persons, expected):
        assert len(persons) == expected
        for p in persons:
            assert p.infected()

    population = Population(20, 1, n_infected)
    verify_infected(population.get_infected(), n_infected)

    while True:
        person = choice(population.people)
        original_status = person.status
        person.infect()
        if person.status != original_status:
            break

    verify_infected(population.get_infected(), n_infected + 1)
