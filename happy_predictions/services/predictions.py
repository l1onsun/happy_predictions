from PIL import Image


class Predictions:
    def get_prediction(self, prediction_id: int, background_name: str) -> Image:
        ...

    def get_random_prediction(self):
        ...
