# Torchtest

A Tiny Test Suite for pytorch based Machine Learning models, inspired by
[mltest](https://github.com/Thenerdstation/mltest/blob/master/mltest/mltest.py).
Chase Roberts lists out 4 basic tests in his [medium
post](https://medium.com/@keeper6928/mltest-automatically-test-neural-network-models-in-one-function-call-eb6f1fa5019d)
about mltest. torchtest is mostly a pytorch port of mltest(which was
written for tensorflow).

--- 

Forked from [BrainPugh](https://github.com/BrianPugh/torchtest) who
forked the repo from
[suriyadeepan](https://github.com/suriyadeepan/torchtest).

Notable changes:

-   Support for models to have multiple positional arguments.

-   Support for unsupervised learning.

-   Fewer requirements (due to streamlining testing).

-   More comprehensive changes.

-   Still active? I've created an
    [issue](https://github.com/suriyadeepan/torchtest/issues/6) to
    double check but it looks like the original maintainer is no longer
    actioning pull requests.

# Installation

``` bash
pip install --upgrade torchtest
```

# Tests

``` python
# imports for examples
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
```

## Variables Change

``` python
from torchtest import assert_vars_change

inputs = Variable(torch.randn(20, 20))
targets = Variable(torch.randint(0, 2, (20,))).long()
batch = [inputs, targets]
model = nn.Linear(20, 2)

# what are the variables?
print('Our list of parameters', [ np[0] for np in model.named_parameters() ])

# do they change after a training step?
#  let's run a train step and see
assert_vars_change(
    model=model,
    loss_fn=F.cross_entropy,
    optim=torch.optim.Adam(model.parameters()),
    batch=batch)
```

``` python
""" FAILURE """
# let's try to break this, so the test fails
params_to_train = [ np[1] for np in model.named_parameters() if np[0] is not 'bias' ]
# run test now
assert_vars_change(
    model=model,
    loss_fn=F.cross_entropy,
    optim=torch.optim.Adam(params_to_train),
    batch=batch)

# YES! bias did not change
```

## Variables Don't Change

``` python
from torchtest import assert_vars_same

# What if bias is not supposed to change, by design?
#  test to see if bias remains the same after training
assert_vars_same(
    model=model,
    loss_fn=F.cross_entropy,
    optim=torch.optim.Adam(params_to_train),
    batch=batch,
    params=[('bias', model.bias)]
    )
# it does? good. let's move on
```

## Output Range

``` python
from torchtest import test_suite

# NOTE : bias is fixed (not trainable)
optim = torch.optim.Adam(params_to_train)
loss_fn=F.cross_entropy

test_suite(model, loss_fn, optim, batch,
    output_range=(-2, 2),
    test_output_range=True
    )

# seems to work
```

``` python
""" FAILURE """
#  let's tweak the model to fail the test
model.bias = nn.Parameter(2 + torch.randn(2, ))

test_suite(
    model,
    loss_fn, optim, batch,
    output_range=(-1, 1),
    test_output_range=True
    )

# as expected, it fails; yay!
```

## NaN Tensors

``` python
""" FAILURE """
model.bias = nn.Parameter(float('NaN') * torch.randn(2, ))

test_suite(
    model,
    loss_fn, optim, batch,
    test_nan_vals=True
    )
```

## Inf Tensors

``` python
""" FAILURE """
model.bias = nn.Parameter(float('Inf') * torch.randn(2, ))

test_suite(
    model,
    loss_fn, optim, batch,
    test_inf_vals=True
    )
```

# Debugging

``` bash
torchtest\torchtest.py", line 151, in _var_change_helper
assert not torch.equal(p0, p1)
RuntimeError: Expected object of backend CPU but got backend CUDA for argument #2 'other'
```

When you are making use of a GPU, you should explicitly specify
`device=cuda:0`. By default `device` is set to `cpu`. See [issue
#1](https://github.com/suriyadeepan/torchtest/issues/1) for more
information.

``` python
test_suite(
    model,  # a model moved to GPU
    loss_fn, optim, batch,
    test_inf_vals=True,
    device='cuda:0'
    )
```

# Citation

``` tex
@misc{Ram2019,
  author = {Suriyadeepan Ramamoorthy},
  title = {torchtest},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/suriyadeepan/torchtest}},
  commit = {42ba442e54e5117de80f761a796fba3589f9b223}
}
```
