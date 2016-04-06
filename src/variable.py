import numpy as np
import gurobipy as grb
from ipdb import set_trace as st

class Variable(object):
    """
    Variable

    Manages Gurobi variables by maintaining an ordering of Gurobi variables,
    """

    def __init__(self, grb_vars):
        """
        _grb_vars: Numpy array of Gurobi variables. The ordering of the Gurobi
        variables must be maintained.
        _value: current value of this variable
        _saved_value: saved value of this variable
        """
        assert isinstance(grb_vars, np.ndarray)
        self._grb_vars = grb_vars.copy()
        self._value = None
        self._saved_value = None

    def get_grb_vars(self):
        return self._grb_vars.copy()

    def get_value(self):
        if self._value is not None:
            return self._value.copy()
        else:
            return None

    def add_trust_region(self, trust_box_size):
        """
        Adds a trust region around the saved value (self._saved_value) by
        changing the upper and lower bounds of the Gurobi variables
        self._grb_vars
        """
        assert self._saved_value is not None
        for index, grb_var in np.ndenumerate(self._grb_vars):
            grb_var.lb = self._saved_value[index] - trust_box_size
            grb_var.ub = self._saved_value[index] + trust_box_size

    def update(self):
        """
        If the gurobi variables have valid values, update self._value to reflect
        the values in the gurobi variables.

        When the gurobi variables do not have valid values, update will raise a
        GurobiError
        """
        value = np.zeros(self._grb_vars.shape)
        for index, grb_var in np.ndenumerate(self._grb_vars):
            value[index] = grb_var.X

        self._value = value

    def save(self):
        """
        Save the current value.

        TODO: remember to unit test that by modifying value you can't change the
        value in self
        """
        self._saved_value = self._value.copy()

    def restore(self):
        """
        Restore value to the saved value.
        """
        self._value = self._saved_value.copy()