from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class ImageDetails:
    image_url: str
    features: Dict[str, Any]
    operations:str

