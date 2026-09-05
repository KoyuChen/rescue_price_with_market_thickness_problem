"""Strict model configuration; solver budgets are explicit command-line inputs."""
from dataclasses import asdict
import json
from pathlib import Path

from .core import ModelParams


def build_model_params(data):
    if not isinstance(data, dict):
        raise ValueError('model must be an object')
    fields = set(ModelParams.__dataclass_fields__)
    unknown = set(data) - fields
    if unknown:
        raise ValueError(f'Unknown model parameters: {sorted(unknown)}')
    values = dict(data)
    for name in ('cost_probability_edges', 'route_positive_quantile_edges'):
        if name in values:
            values[name] = tuple(values[name])
    return ModelParams(**values)


def load_config(path=None):
    if path is None:
        return {'model': asdict(ModelParams())}
    data = json.loads(Path(path).read_text())
    if not isinstance(data, dict) or set(data) != {'model'}:
        raise ValueError('Config must contain exactly one top-level key: model; no hidden solver budgets')
    return {'model': asdict(build_model_params(data['model']))}
