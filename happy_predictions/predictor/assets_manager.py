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


class MissingAsset(Exception):
    ...


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
        return {
            i: convert_at_sign(values[0])
            for i, values in enumerate(predictions_skip_header)
        }

    @staticmethod
    def _load_backgrounds() -> dict[str, Image]:
        backgrounds: dict[str, Image] = {}
        for img_name in os.listdir(BACKGROUNDS_PATH):
            img_path = os.path.join(BACKGROUNDS_PATH, img_name)
            backgrounds[img_name] = Image.open(img_path)
            log.debug(f"open background {img_path}")
        return backgrounds

    def list_available_backgrounds(self) -> list[str]:
        return list(self._backgrounds.keys())

    def list_available_text_ids(self) -> list[int]:
        return list(self._prediction_texts.keys())

    def random_prediction_text_id(self) -> int:
        return random.choice(self.list_available_text_ids())

    def random_background_name(self) -> str:
        return random.choice(self.list_available_backgrounds())

    def get_prediction_text(self, text_id: int) -> str:
        try:
            return self._prediction_texts[text_id]
        except KeyError:
            raise MissingAsset(f"No text with {text_id=}")

    def get_background(self, name: str) -> Image:
        try:
            return self._backgrounds[name]
        except KeyError:
            raise MissingAsset(f"No background with {name=}")

    def get_font(self, size: int) -> ImageFont:
        return self._fonts.get(size) or self._load_font(size)

    def _load_font(self, size: int) -> ImageFont:
        font = ImageFont.truetype(FONT_PATH, size=size)
        self._fonts[size] = font
        return font


def convert_at_sign(text_with_at_signs: str) -> str:
    return text_with_at_signs.replace("@", "\n")
