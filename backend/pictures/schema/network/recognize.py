from .image_handler import ImageHandler
from pybrain.tools.customxml.networkreader import NetworkReader
import os


def get_numbers(image_file):
    image_handler = ImageHandler(image_file)
    numbers = image_handler.number_data
    numbers.sort(key=lambda x: x['position'][0])

    output_data = []
    dir = os.path.dirname(__file__)
    net = NetworkReader.readFrom(dir + '/num_network.xml')
    for number in numbers:
        results = net.activate(number['data'])
        ds = list(map(lambda x: abs(x - 1), results))
        index = ds.index(min(ds))
        number['number'] = index
        output_data.append(index)
    return numbers, output_data


if __name__ == '__main__':
    get_numbers('./../image_handler/images/image_4.png')
