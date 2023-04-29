from time import time
from flask import Flask, request, jsonify
from flask_restful import Api, reqparse
import indisim_mutual as sim
from indisim_mutual import realtime_data
from flask_cors import CORS
import numpy as np
from json import JSONEncoder, loads, dumps
import pandas as pd
import os
import shutil


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


REALTIME_DATA = ""


def run_simulator(sessionid):
    data = loads(request.data.decode("utf-8"))
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
        population=test_p, media=test_m, history=test_history, sessionid=sessionid)

    # Get the species from the data payload arguments
    population_args_keys = population_args.keys()
    species_nonzero = []
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
    # Run the simulator
    test_s.experiment(
        transfer_p=run_args["transfer_p"], transfer_frequency=run_args["days"], n_initial=0, n_transfer=1, show_progress=False)
    print("-----------------------------end-----------------------------")

    # Get the number of days from the history array
    n = len(test_history.p)
    counts = []
    encodedNumpyData = []
    responseData = []

    # Count the species from the history array and convert them into a JSON format
    for i in range(0, n, 1):
        counts.append(test_history.p[i][:, -1])
        encodedNumpyData = dumps(
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

        #  Map the alive species with the available data
        for j in range(len(species_distribution)):
            spec = species_nonzero[int(species_distribution[j])-1]
            alive_species.append(spec)

        # Check if the species is repeated and append the count to the species name
        op = {}
        isRepeated = {}
        # Append the media data to the JSON
        media_dict = {"glucose": test_history.s[i],
                      "adenine": test_history.sa[i],
                      "lysine": test_history.sl[i], }
        for i in range(len(alive_species)):
            if alive_species[i] in isRepeated:
                isRepeated[alive_species[i]] += 1
                alive_species[i] = alive_species[i] + \
                    str(isRepeated[alive_species[i]])
            else:
                isRepeated[alive_species[i]] = 1
                alive_species[i] = alive_species[i] + str(1)
            op[alive_species[i]] = pop[i]

        merged_dict = {**op, **media_dict}
        responseData.append(merged_dict)

    # Create a folder to store the CSV file
    path = os.path.abspath(f'csv/{sessionid}')
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)

    #  Save the data to a CSV file
    df = pd.DataFrame(responseData)
    df.to_csv(f'{path}/output.csv', index=True)

    path = os.path.abspath(f'realtime/{sessionid}')
    # Delete the realtime data
    if os.path.exists(path):
        shutil.rmtree(path)

    return {"responseData": responseData}
