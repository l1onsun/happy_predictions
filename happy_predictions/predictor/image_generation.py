from dataclasses import InitVar, dataclass, field
from functools import lru_cache
from typing import TypeAlias

from PIL import Image, ImageDraw, ImageFont

from happy_predictions.predictor.assets_manager import AssetsBox

IMAGE_CACHE_LEN = 10
OUTLINE_SHIFT_TO_FONT_RATIO = 50
FONT_SIZE_TO_WIDTH_RATIO = 13
TEXT_COLOR = (255, 255, 255)
OUTLINE_COLOR = (0, 0, 0)

Position: TypeAlias = tuple[int, int]


@dataclass(frozen=True)
class PredictionParams:
    text_id: int
    background_name: str


@dataclass
class TextWithOutlineDrawer:
    text: str
    font: ImageFont
    font_size: int
    background: InitVar[Image]
    output_image: Image = field(init=False)
    image_draw: ImageDraw = field(init=False)
    outline_draw_positions: list[Position] = field(init=False)
    center: Position = field(init=False)

    def __post_init__(self, background: Image):
        self.output_image = background.copy()
        self.image_draw = ImageDraw.Draw(self.output_image)
        self.center = self.output_image.width // 2, self.output_image.height // 2
        outline_shift = self.font_size // OUTLINE_SHIFT_TO_FONT_RATIO
        self.outline_draw_positions = [
            (self.center[0] - outline_shift, self.center[1]),
            (self.center[0], self.center[1] + outline_shift),
            (self.center[0] + outline_shift, self.center[1]),
            (self.center[0], self.center[1] - outline_shift),
        ]

    def draw(self):
        for pos in self.outline_draw_positions:
            self._draw_text(pos, OUTLINE_COLOR)
        self._draw_text(self.center, TEXT_COLOR)
        return self.output_image

    def _draw_text(self, pos: Position, color: tuple[int, int, int]):
        self.image_draw.text(
            pos, self.text, font=self.font, fill=color, anchor="mm", align="center"
        )


@dataclass
class ImageGenerator:
    assets: AssetsBox

    def gen_image(self, prediction_params: PredictionParams) -> Image:
        background = self.assets.get_background(prediction_params.background_name)
        font_size = background.width // FONT_SIZE_TO_WIDTH_RATIO

        return TextWithOutlineDrawer(
            text=self.assets.get_prediction_text(prediction_params.text_id),
            background=background,
            font=self.assets.get_font(font_size),
            font_size=font_size,
        ).draw()

    @lru_cache(maxsize=IMAGE_CACHE_LEN)
    def gen_image_cached(self, prediction_params: PredictionParams):
        return self.gen_image(prediction_params)
