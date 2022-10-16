import numpy as np

class ObservableMatrix(np.ndarray):
    prev_matrix = None
    def __new__(self, input_array, onupdate_func = None):
        self.onupdate_func = onupdate_func
        return np.asarray(input_array).view(self)

    def __getitem__(self, key):
        if self.prev_matrix is None:
            self.prev_matrix = self.copy()
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        self.prev_matrix = self.copy()
        super().__setitem__(key, value)
        if self.onupdate_func:
            self.onupdate_func()
        self.prev_matrix = None
        return None

