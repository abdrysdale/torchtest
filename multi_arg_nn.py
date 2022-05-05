"""Class for a neural network with multiple arguments."""
#! /usr/bin/env python

# Python imports
import collections

# Module imports
import torch

class multi_arg_nn(torch.nn.Module):
    def __init__(self, layers, **kwargs):
        """Neural network class with multiple positional arguments

        Args:
            layers (list) : A list of the size of each layer.

        Kwargs:
            activation (torch.nn activation function) : Module activation function.
                Defaults to torch.nn.ReLU
            device (str) : Device to store tensors. Defaults to "cpu".
        """

        # Keyword arguments
        self.activation = kwargs.get("activation", torch.nn.ReLU)
        device = kwargs.get("device", "cpu")

        # Parameters
        self.depth = len(layers) - 1

        # Set up network layers
        layer_list = []
        for i in range(self.depth - 1):
            layer_list.append(
                (f"layer_{i}", torch.nn.Linear(layers[i], layers[i+1]))
            )
            layer_list.append((f"activation_{i}", self.activation()))

        layer_list.append(
            (f"layer_{self.depth - 1}", torch.nn.Linear(layers[-2], layers[-1]))
        )
        layer_dict = collections.OrderedDict(layer_list)

        self.layers = torch.nn.Sequential(layer_dict)


    def forward(self, arg_1, arg_2):
        nn_input = torch.cat((arg_1, arg_2))
        return self.layers(nn_input)
