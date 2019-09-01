# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module contains unit tests for testing the mlopt.blending.ParticleSwarmOptimizer class."""

import numpy as np

from mlopt.optimization import ParticleSwarmOptimizer


def opt_func(*args):
    """Function for minimization testing."""
    return sum(arg**2 for arg in args)


def opt_func_inv(*args):
    """Function for maximization testing."""
    return - opt_func(*args)


def test_init_correct_dimensions_velocities():
    """Test if the initialized velocities have the correct dimension."""
    pso = ParticleSwarmOptimizer(func=opt_func, maximize=False, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)

    assert pso._velocities.shape == (20, 2)


def test_init_correct_dimensions_coords():
    """Test if the initialized coordinates have the correct dimension."""
    pso = ParticleSwarmOptimizer(func=opt_func, maximize=False, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)

    assert pso._coords_all.shape == (20, 2)


def test_init_correct_dimensions_best_coords():
    """Test if the initialized best coordinates of each particle have the correct dimensions."""
    pso = ParticleSwarmOptimizer(func=opt_func, maximize=False, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)

    assert pso._best_coords_all.shape == (20, 2)


def test_init_correct_dimensions_best_coords_glob():
    """Test if the initialized best coordinates of all particles combined have the correct dimensions."""
    pso = ParticleSwarmOptimizer(func=opt_func, maximize=False, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)

    assert pso.coords.shape == (2,)


def test_init_correct_dimensions_best_scores():
    """Test if the initialized best scores of each particle have the correct dimensions."""
    pso = ParticleSwarmOptimizer(func=opt_func, maximize=False, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)

    assert len(pso._score_all) == 20


def test_init_correct_dimensions_best_score_glob():
    """Test if the initialized best score of all particles have the correct dimension."""
    pso = ParticleSwarmOptimizer(func=opt_func, maximize=False, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)
    print('best score', pso.score)
    assert np.shape(pso.score) == ()


def test_init_deterministic_random_state():
    """Test if the initialized coordinates are deterministic if random state is fixed."""
    pso = ParticleSwarmOptimizer(func=opt_func, maximize=False, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)
    coords0 = pso._coords_all
    pso.init(params=params, random_state=1)
    coords1 = pso._coords_all

    assert all(val0 == val1 for row0, row1 in zip(coords0, coords1) for val0, val1 in zip(row0, row1))


def test_init_different_random_state():
    """Test if the initialized coordinates are not deterministic if random state is not fixed."""
    pso = ParticleSwarmOptimizer(func=opt_func, maximize=False, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)
    coords0 = pso._coords_all
    pso.init(params=params, random_state=2)
    coords1 = pso._coords_all

    assert any(val0 != val1 for row0, row1 in zip(coords0, coords1) for val0, val1 in zip(row0, row1))


def test_update_monotonic_best_score_glob_minimize():
    """Test if the particle swarm optimizer monotonically converges for minimization problems."""
    pso = ParticleSwarmOptimizer(func=opt_func, maximize=False, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)

    scores = [pso.score]
    for i in range(100):
        pso.update(params)
        scores.append(pso.score)

    assert all(scores[i+1] <= scores[i] for i in range(len(scores)-1))


def test_update_monotonic_best_scores_minimize():
    """Test if each particle of the particle swarm optimizer monotonically converges for minimization problems."""
    pso = ParticleSwarmOptimizer(func=opt_func, maximize=False, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)

    scores = {p: [pso._score_all[p]] for p in range(20)}
    for i in range(100):
        pso.update(params)
        for particle in range(20):
            scores[particle] = scores[particle] + [pso._score_all[particle]]

    assert all(all(scores[particle][i+1] <= scores[particle][i] for i in range(len(scores[particle])-1))
               for particle in range(20))


def test_update_monotonic_best_score_glob_maximize():
    """Test if the particle swarm optimizer monotonically converges for maximization problems."""
    pso = ParticleSwarmOptimizer(func=opt_func_inv, maximize=True, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)

    scores = [pso.score]
    for i in range(100):
        pso.update(params)
        scores.append(pso.score)

    assert all(scores[i+1] >= scores[i] for i in range(len(scores)-1))


def test_update_monotonic_best_scores_maximize():
    """Test if each particle of the particle swarm optimizer monotonically converges for maximization problems."""
    pso = ParticleSwarmOptimizer(func=opt_func_inv, maximize=True, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.init(params=params, random_state=1)

    scores = {p: [pso._score_all[p]] for p in range(20)}
    for i in range(100):
        pso.update(params)
        for particle in range(20):
            scores[particle] = scores[particle] + [pso._score_all[particle]]

    assert all(all(scores[particle][i+1] >= scores[particle][i] for i in range(len(scores[particle])-1))
               for particle in range(20))


def test_coord_history_correct_dimension():
    """Test if the saved particles coordinate history has the correct dimensions."""
    pso = ParticleSwarmOptimizer(func=opt_func, maximize=False, particles=20)

    params = {'x': (-1, 1), 'y': (-1, 1)}
    pso.optimize(params, iterations=20)

    history = pso.coords_history

    assert len(history) == 21
    assert all(history[i].shape == (20, 2) for i in range(20))
