# Constraint Opinion Models

Constraint Opinion Models extend the standard DeGroot model by representing
agents' opinions and influences as soft constraints rather than single real
values. This allows for modeling scenarios beyond the scope of the DeGroot
model, such as agents sharing partial information and preferences, engaging in
discussions on multiple topics simultaneously, and representing opinions with
different degrees of uncertainty. By considering soft constraints as
influences, the proposed model captures also situations where agents impose
conditions on how others' opinions are integrated during belief revision.
Constraint Opinion Models are equipped with a polarization measure that
determines the distance between opinions. 

This repository contains a proof of concept for experimenting with Constraint
Opinion Models. 

More details can be found in this [paper](./paper.pdf).

## Getting Stated
The scripts were tested with [Python 3.13](https://www.python.org/). Some
dependencies are needed that can be installed with pip (see file
`requirements.txt`). 

## Files

See more information in the header of each file

- `semiring.py`: Definition of a semiring and the lifiting operations to build
  the semiring on constraints
- `models.py`: Matrix multiplication based on the semiring and updating the
  vector of opinions. 
- `exR.py`: A simple example using R+
- `exBool.py`: A simple example using Bool
- `exCommitee.py`: Example of agents deciding on the number of agents to form a
  selection committee. See the complete description in the
  [paper](./paper.pdf). 
- `exOpinion.py`: Agents express their preferences using a Likert scale
- `exExtremes.py`: Agents expressing extreme and moderate point of views
- `exSeveralOps.py`: Agents discussing about different topics at the same time

The Jupyter Notebook `Experiments.ipynb` can be used to generate the plots in
the paper. 
