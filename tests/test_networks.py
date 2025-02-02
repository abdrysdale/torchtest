"""Class for a test neural networks."""
#! /usr/bin/env python

# Python imports
import collections

# Module imports
import torch

class SingleArgRegression(torch.nn.Module):
    """Single argument input (deep) neural network block"""
    def __init__(self, layers):
        """Neural network class with a single positional arguments

        Parameters
        ----------
            layers : list
                A list of the size of each layer.
        """
        super().__init__()

        # Activation function
        self.activation = torch.nn.ReLU

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


    def forward(self, nn_input):
        """Forward pass"""
        return self.layers(nn_input)


class MultiArgRegression(torch.nn.Module):
    """Multiple argument input (deep) neural network block"""
    def __init__(self, layers):
        """Neural network class with multiple positional arguments

        Parameters
        ----------
            layers : list
                A list of the size of each layer.

        """
        super().__init__()
        self.layers = SingleArgRegression(layers)

    def forward(self, arg_1, arg_2):
        """Forward pass"""
        nn_input = torch.cat((arg_1, arg_2), dim=1)
        return self.layers(nn_input)

class MultiOutputRegression(torch.nn.Module):
    """Multiple output neural network block"""
    def __init__(self, layers, num_outputs=2):
        """Neural network class with multiple outputs

        Parameters
        ----------
            layers : list
                A list of the size of each layer.
            num_outputs : int, optional
                The number of neural network ouptuts.
                Defaults to 2.

        """
        super().__init__()
        nets = []
        for _ in range(num_outputs):
            nets.append(SingleArgRegression(layers))
        self.nets = torch.nn.ModuleList(nets)

    def forward(self, x):
        return [net(x) for net in self.nets]

class SingleArgClassification(torch.nn.Module):
    """Single argument input (deep) neural network classification network"""
    def __init__(self, layers):
        """
        Parameters
        ----------
            layers : list
                A list of the size of each layer.

        """
        super().__init__()
        self.layers = SingleArgRegression(layers)
        self.activation = torch.sigmoid

    def forward(self, nn_input):
        """Forward pass"""
        return self.activation(self.layers(nn_input))

class InfModel(torch.nn.Module):
    """Model that always returns infinite"""
    def __init__(self, layers):
        """
        Parameters
        ----------
            layers : list
                A list of the size of each layer.

        """
        super().__init__()
        self.layers = SingleArgRegression(layers)

    def forward(self, nn_input):
        """Forward pass"""
        output = self.layers(nn_input) * float('inf')
        return output
