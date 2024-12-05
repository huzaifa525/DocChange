from dataclasses import dataclass, field
from typing import Dict, List
import numpy as np

@dataclass
class Document:
    content: str
    metadata: Dict = field(default_factory=dict)
    chunks: List[str] = field(default_factory=list)
    embeddings: np.ndarray = field(default_factory=lambda: np.array([]))