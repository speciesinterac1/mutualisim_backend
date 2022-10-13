from time import time
from flask import Flask, json, request, jsonify
from flask_restful import Api, reqparse
import indisim_mutual as sim
from indisim_mutual import realtime_data
from flask_cors import CORS
import numpy as np
from json import JSONEncoder
from clean import clean_population_data


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


REALTIME_DATA = ""


def run_simulator():
    data = json.loads(request.data.decode("utf-8"))
    population_args = data['population']
    media_args = data['media']
    run_args = data['run']
    test_p = sim.loadoc.initiate_community(adeop=population_args["adeop"], lysop=population_args["lysop"], adewt=population_args["adewt"], lyswt=population_args["lyswt"],
                                           n_adeop=population_args["n_adeop"], n_lysop=population_args[
                                               "n_lysop"], n_adewt=population_args["n_adewt"], n_lyswt=population_args["n_lyswt"],
                                           folder='./unit_development/OC')
    test_m = sim.Media(dimension=(
        7, 7, 7), glucose=media_args["glucose"], ade=media_args["adenine"], lys=media_args["lysine"])
    test_history = sim.History()
    test_s = sim.Simulator(
        population=test_p, media=test_m, history=test_history)

    population_args_keys = population_args.keys()
    species_nonzero = []
    # Get the species from the data payload arguments
    for key in population_args_keys:
        n = population_args[key]
        if n == 0:
            species_nonzero
        else:
            for i in range(0, n):
                if (key[0] != "n"):
                    species_nonzero.append(key)

    print(population_args)
    print("-----------------------------start-----------------------------")

    test_s.experiment(
        transfer_p=run_args["transfer_p"], n_initial=0, n_transfer=1, show_progress=False)
    print("-----------------------------end-----------------------------")

    n = len(test_history.p)
    counts = []
    tests = []
    encodedNumpyData = []
    responseData = []

    # Count the species from the history array and convert them into a JSON format
    for i in range(0, n, 1):
        counts.append(test_history.p[i][:, -1])
        encodedNumpyData = json.dumps(
            np.unique(counts[i], return_counts=True), cls=NumpyArrayEncoder)
        splitarr = encodedNumpyData.split("], ")
        species_distribution = encodedNumpyData.split(
            ", [")[0].strip("[]").split(", ")
        ar = []
        pop = []
        alive_species = []
        for l in splitarr:
            ar = l.split("], ")
            for d in ar:
                pop = d[:-1].strip('][').split(', ')
        tests.append(pop)

        #  Map the alive species with the available data
        for j in range(len(species_distribution)):
            spec = species_nonzero[int(species_distribution[j])-1]
            alive_species.append(spec)

        responseData.append([species_distribution, alive_species, pop])
        # clean_data = clean_population_data(alive_species, pop)
        # responseData.append(clean_data)

    # print(alive_species, pop)

    # return {"species": test_p.get_species(), "population": test_s.get_n(), "glucose": test_history.s, "adenine": test_history.sa, "lysine": test_history.sl}
    return {"responseData": responseData}
