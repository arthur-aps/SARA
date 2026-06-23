from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class AudioChunk:
    samples: np.ndarray
    rms: float