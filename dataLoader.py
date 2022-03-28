import h5py
import numpy as np
import re

class DataLoader:

    def __init__(self, filename="task_data.hdf5"):
        self.filename = filename 

    def get_data(self,hour, dataset):
        with h5py.File(self.filename, "r") as h5:

            if f'results/{hour}/{dataset}' in h5:
                data_h5 = h5.get(f'results/{hour}/{dataset}')
                data = np.zeros(data_h5.shape, dtype=data_h5.dtype)
                data_h5.read_direct(data)

                return data
            raise "Wrong value of dataset or folder, not exist in h5 file"
            
    def load_hours_from_h5(self):
        def atoi(text):
            return int(text) if text.isdigit() else text

        def natural_sorting(text):
            return [ atoi(c) for c in re.split(r'(\d+)', text) ]

        with h5py.File(self.filename, "r") as h5:
            hours = [key for key in h5.get('results').keys()]
            hours.sort(key=natural_sorting)
            return hours