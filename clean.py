op = {}
isRepeated = {}


def clean_population_data(alive_species, pop):
    for i in range(len(alive_species)):
        if alive_species[i] in isRepeated:
            isRepeated[alive_species[i]] += 1
            alive_species[i] = alive_species[i]+str(1)
        else:
            isRepeated[alive_species[i]] = 1

        op[alive_species[i]] = pop[i]
    return op
