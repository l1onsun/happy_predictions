from functools import lru_cache
import csv
import random
import img_gen
import io
import os

@lru_cache
def load_predictions():
    return open("assets/2021_drive.csv", 'r')

@lru_cache
def get_predictions():
    return list(csv.reader(load_predictions(), delimiter = ','))

# def _gen_img_by_prediction_idx(index):
#     predictions = get_predictions()
#     text = predictions[index][0].replace("@", "\n")
#     img = img_gen.insert_text_center('assets/backgrounds/b1.jpg', 'arial.ttf', text)
#     memory_img = io.BytesIO()
#     img.save(memory_img, format='jpeg')
#     memory_img.seek(0)
#     return memory_img


def get_random_prediction():
    predictions = get_predictions()
    index = random.randrange(len(predictions))
    return index, *get_prediction(index)

def get_prediction(index: int, background = None):

    random_background = None
    if background == None:
        available_backgrounds = os.listdir('assets/backgrounds')
        random_background = random.choice(available_backgrounds)
        print("random: ", random_background)

    predictions = get_predictions()
    text = predictions[index][0].replace("@", "\n")
    print("pre pre generate")
    img = img_gen.insert_text_center('assets/backgrounds/' + (background or random_background), 'assets/arial.ttf', text)
    print("after insert")
    memory_img = io.BytesIO()
    img.save(memory_img, format='jpeg')
    memory_img.seek(0)
    print("end generate")

    if background:
        return memory_img
    else:
        return random_background, memory_img

