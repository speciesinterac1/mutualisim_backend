from collections import Counter
from json import JSONEncoder, loads, dumps
import pandas as pd

# Convert the data into the following format
# responseData = [
#     [
#         "1",
#         "2",
#         "3",
#         "4",
#         "5",
#         "6",
#         "7",
#         "8"
#     ],
#     [
#         "adeop",
#         "adeop",
#         "lysop",
#         "lysop",
#         "adewt",
#         "adewt",
#         "lyswt",
#         "lyswt"
#     ],
#     [
#         "10",
#         "10",
#         "10",
#         "10",
#         "20",
#         "20",
#         "20",
#         "20"
#     ]
# ]

# responseData = [species_distribution, alive_species, pop]

# responseData = [ {
#     "adeop1": "28",
#     "adeop2": "25",
#     "lysop1": "47",
#     "lysop2": "28",
#     "adewt1": "74",
#     "adewt2": "99",
#     "lyswt1": "86",
#     "lyswt2": "52"
# } ]


# Convert the data into the following format
op = {}
isRepeated = {}


def transform_data(alive_species, pop):
    # Count the occurrences of each species name
    for i in range(len(alive_species)):
        if alive_species[i] in isRepeated:
            isRepeated[alive_species[i]] += 1
            alive_species[i] = alive_species[i] + \
                str(isRepeated[alive_species[i]])
        else:
            isRepeated[alive_species[i]] = 1
            alive_species[i] = alive_species[i] + str(1)
        op[alive_species[i]] = pop[i]
    return op


data = [{
    "cycle": "1",
    "adeop1": "5",
    "adeop2": "5",
    "adewt1": "11",
    "adewt2": "9",
    "lysop1": "5",
    "lysop2": "8",
    "lyswt1": "9",
    "lyswt2": "11"
},
    {
    "cycle": "1",
    "adeop1": "5",
    "adeop2": "5",
    "adewt1": "11",
    "adewt2": "9",
    "lysop1": "5",
    "lysop2": "8",
    "lyswt1": "9",
    "lyswt2": "11"
},
    {
    "cycle": "1",
    "adeop1": "5",
    "adeop2": "5",
    "adewt1": "11",
    "adewt2": "9",
    "lysop1": "5",
    "lysop2": "8",
    "lyswt1": "9",
    "lyswt2": "11"
},
    {
    "cycle": "1",
    "adeop1": "5",
    "adeop2": "5",
    "adewt1": "11",
    "adewt2": "9",
    "lysop1": "5",
    "lysop2": "8",
    "lyswt1": "9",
    "lyswt2": "11"
}]


def json_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('output.csv', index=True)

    print(df)

    # df = df[[keys]]
    # df.to_csv('output.csv', header=[data[0].keys()],
    #           index=range(len(data[0].keys())))


json_to_csv()


def clean_population_data(alive_species, pop):
    for i in range(len(alive_species)):
        if alive_species[i] in isRepeated:
            isRepeated[alive_species[i]] += 1
            alive_species[i] = alive_species[i]+str(1)
        else:
            isRepeated[alive_species[i]] = 1

        op[alive_species[i]] = pop[i]
    return op
