import csv
import os
import random
from dataclasses import dataclass

import structlog
from PIL import Image, ImageFont

from happy_predictions.const import YEAR

PREDICTIONS_CSV_PATH = f"assets/{YEAR}_drive.csv"
BACKGROUNDS_PATH = "assets/backgrounds"
FONT_PATH = "assets/arial.ttf"

log = structlog.get_logger()


@dataclass
class AssetsBox:
    _prediction_texts: dict[int, str]
    _backgrounds: dict[str, Image]
    _fonts: dict[int, ImageFont]

    @classmethod
    def load_assets(cls) -> "AssetsBox":
        return cls(
            _prediction_texts=cls._load_prediction_texts(),
            _backgrounds=cls._load_backgrounds(),
            _fonts={},
        )

    @staticmethod
    def _load_prediction_texts() -> dict[int, str]:
        with open(PREDICTIONS_CSV_PATH, "r") as file:
            predictions_raw = list(csv.reader(file, delimiter=","))
        predictions_skip_header = predictions_raw[1:]
        return {i: values[0] for i, values in enumerate(predictions_skip_header)}

    @staticmethod
    def _load_backgrounds() -> dict[str, Image]:
        backgrounds: dict[str, Image] = {}
        for img_name in os.listdir(BACKGROUNDS_PATH):
            img_path = os.path.join(BACKGROUNDS_PATH, img_name)
            backgrounds[img_name] = Image.open(img_path)
            log.debug(f"open background {img_path}")
        return backgrounds

    def random_prediction_text_id(self) -> int:
        return random.choice(list(self._prediction_texts.keys()))

    def random_background_name(self) -> str:
        return random.choice(list(self._backgrounds.keys()))

    def get_prediction_text(self, text_id: int) -> str:
        return self._prediction_texts[text_id]

    def get_background(self, name: str) -> Image:
        return self._backgrounds[name]

    def get_font(self, size: int) -> ImageFont:
        return self._fonts.get(size) or self._load_font(size)

    def _load_font(self, size: int) -> ImageFont:
        font = ImageFont.truetype(FONT_PATH, size=size)
        self._fonts[size] = font
        return font
