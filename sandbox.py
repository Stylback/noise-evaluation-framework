import pandas as pd
import numpy as np
from data import main as data
from Filters.TestFilter import FilterCoa
from evaluation import ml

def main():

    results = []

    # for number of caseids
    for caseid in range(len(data.caseids)):
        print (range(len(data.caseids)))

        if caseid == 9 or caseid == 17 or caseid == 24 or caseid == 27 or caseid == 28:
            continue

        # pull waveform
        waveform = data.get_waveform(
                data.caseids[caseid], data.track_names[0], timestamp=True, dropna=True, interval=1/100)
        
        # Run filter
        filtered_waveform = FilterCoa.Filter_delete(waveform)

        # Define File Directory
        directory = 'C:\\Users\\axelm\\Documents\\1. School - KTH\\Year 1\\S1 P1&2\\CM2015 Project Carrier Course for Medical Engineers\\Project\\VSCode Workspace\\HealthSyS\\machineLearning\\'
        modelName = "lee_model_matched.hdf5"

        # Extract signal data
        original_signal = [data[0] for data in waveform]
        filtered_signal = [data[0] for data in filtered_waveform]

        # Run ml function
        results.append(ml.mlMain(directory, modelName, original_signal, filtered_signal, 2500))
        print(caseid)
        print(results)

    # print results
    print(f"Final: {results}")

main()


