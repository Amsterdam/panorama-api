import io

from urllib.request import urlopen

from django.conf import settings

from PIL import Image

from panorama.shared.object_store import ObjectStore

PANORAMA_WIDTH = 8000
PANORAMA_HEIGHT = 4000
SAMPLE_WIDTH = 480
SAMPLE_HEIGHT = 320

object_store = ObjectStore()


def byte_array2image(byte_array):
    """
    Translate byte array to PIL image
    :param byte_array:
    :return: PIL image
    """
    return Image.open(io.BytesIO(byte_array))


def get_raw_panorama_image(panorama_path):
    """
    Gets the un-rendered, un-blurred source image from the source container

    :param panorama_path: path of the image
    :return: PIL image
    """

    # construct objectstore_id
    container = panorama_path.split("/")[0]
    name = panorama_path.replace(container + "/", "")
    objectstore_id = {"container": container, "name": name}

    return byte_array2image(object_store.get_panorama_store_object(objectstore_id))


def get_panorama_image(panorama_path):
    """
    Gets the rendered, blurred result image of the panorama

    :param panorama_path: path of the image
    :return: PIL image

    """

    response = urlopen(f"{settings.PANO_IMAGE_URL}/{panorama_path}")
    imdata = response.read()

    return byte_array2image(imdata)


def roll_left(image, shift, width, height):
    """
    Utility method to wrap an image around to the left

    :param image: PIL image to wrap around
    :param shift: the amount of pixels to shift
    :param width:  width of the image
    :param height: height of the image
    :return: shifted PIL image
    """
    part1 = image.crop((0, 0, shift, height))
    part2 = image.crop((shift, 0, width, height))
    part1.load()
    part2.load()
    output = Image.new("RGB", (width, height))
    output.paste(part2, (0, 0, width - shift, height))
    output.paste(part1, (width - shift, 0, width, height))

    return output


def sample_image(image, x, y, sample_width=SAMPLE_WIDTH, sample_height=SAMPLE_HEIGHT):
    """
    Utility method to take a sample from an image

    :param image: PIL image to sample from
    :param x: left-top-x of sample
    :param y: left-top-y of sample
    :param sample_width: width of sample
    :param sample_height: height of sample
    :return:
    """
    if PANORAMA_WIDTH < x + sample_width:
        intermediate = roll_left(image, sample_width, PANORAMA_WIDTH, PANORAMA_HEIGHT)
        snippet = intermediate.crop((x - sample_width, y, x, y + sample_height))
    else:
        snippet = image.crop((x, y, x + sample_width, y + sample_height))
    return snippet
