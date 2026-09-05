from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json
import os
import tempfile
import hashlib
import platform

import numpy as np

from .core import Profile


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_identity():
    root = Path(__file__).resolve().parent
    return dict(economic_baseline='v1.1.1',
        source_sha256={p.name: digest(p) for p in sorted(root.glob('*.py'))},
        numpy_version=np.__version__, python_version=platform.python_version(),
        v12_candidates_imported=False)


def atomic_write_json(path: str | Path, data: Dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, sort_keys=True, allow_nan=False)
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def save_profile(path: str | Path, profile: Profile) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            np.savez_compressed(
                handle,
                sigma_e=profile.sigma_e,
                sigma_h=profile.sigma_h,
                retain=profile.retain,
                q_values=profile.q_values,
                meta_json=np.asarray(json.dumps(profile.meta, sort_keys=True)),
            )
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def load_profile(path: str | Path) -> Profile:
    with np.load(Path(path), allow_pickle=False) as data:
        meta = json.loads(str(data["meta_json"].item()))
        return Profile(
            sigma_e=np.asarray(data["sigma_e"]),
            sigma_h=np.asarray(data["sigma_h"]),
            retain=np.asarray(data["retain"]),
            q_values=np.asarray(data["q_values"]),
            meta={str(k): float(v) for k, v in meta.items()},
        )
