import io
from dataclasses import dataclass

from happy_predictions.predictor.assets_manager import AssetsBox
from happy_predictions.predictor.image_generation import (
    ImageGenerator,
    PredictionParams,
)


@dataclass
class Predictor:
    image_gen: ImageGenerator
    assets: AssetsBox

    def get_image(self, params: PredictionParams) -> io.BytesIO:
        bytes_io = self.image_gen.gen_image_cached(params)
        bytes_io.seek(0)
        return bytes_io

    def gen_custom_image(self, background_name: str, text: str) -> io.BytesIO:
        bytes_io = self.image_gen.gen_custom_image(
            self.assets.get_background(background_name), text
        )
        bytes_io.seek(0)
        return bytes_io

    def get_random_prediction_params(self) -> PredictionParams:
        return PredictionParams(
            text_id=self.assets.random_prediction_text_id(),
            background_name=self.assets.random_background_name(),
        )
