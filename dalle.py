import os

from BingImageCreator import ImageGenAsync, async_image_gen

bing_cookie = os.getenv("BING_COOKIE")

IMG_GEN = ImageGenAsync(auth_cookie=bing_cookie)


def prompt(price_change: float) -> str:
    if price_change > 1:
        return "A cheerful anime girl enjoying a warm and sunny day, with a bright smile on her face, symbolizing a stock rise of more than 1%. "
    elif -1 < price_change < 1:
        return "A neutral anime girl with a calm expression, symbolizing a stable stock market. "
    else:
        return "An illustration of a saddened anime girl sitting on the edge of a broken arrow pointing downwards, under a stormy sky, symbolizing a significant tumble in the stock. "


async def gen_mood_pic(prompt: str):
    result = await IMG_GEN.get_images(prompt)
    return result
