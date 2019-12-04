from PIL import Image
import numpy
import itertools


class ImageHandler:
    def __init__(self, img_path):
        self.used_pixel = []

        image = Image.open(img_path).convert('L')
        self.image_arr = numpy.array(image)
        self.width, self.height = self.image_arr.shape

        self._contrast_image_arr()
        self.numbers = self.get_numbers()

        self.number_data = []
        for index, number in enumerate(self.numbers):
            top = min(number, key=lambda x: x[0])[0]
            bottom = max(number, key=lambda x: x[0])[0]
            left = min(number, key=lambda x: x[1])[1]
            right = max(number, key=lambda x: x[1])[1]

            width = right - left
            height = bottom - top

            if width > height:
                plus = (width - height)/2
                top = top - plus
                bottom = bottom + plus
            else:
                plus = (height - width)/2
                left = left - plus
                right = right + plus

            new_image = image.crop((left, top, right, bottom))
            # new_image.save('./handler_proccess/{}.png'.format(index))
            new_image = new_image.resize((30, 30), Image.ANTIALIAS)

            new_image_arr = numpy.array(new_image).reshape(-1)
            self.number_data.append({
                'image': new_image,
                'position': (left, top, right, bottom),
                'data': new_image_arr
            })



    def _contrast_image_arr(self):
        for i, j in itertools.product(range(self.width), range(self.height)):
            self.image_arr[i][j] = 255 if self.image_arr[i][j] > 128 else 0

    def get_numbers(self):
        numbers = []

        for i, j in itertools.product(range(self.width), range(self.height)):
            print(i, j)
            number = self.get_number((i, j))
            if number:
                numbers.append(number)

        return numbers

    def get_number(self, pixel):
        if pixel in self.used_pixel:
            return None

        if self.image_arr[pixel[0]][pixel[1]] == 255:
            return None

        all_pixels = []
        neighbourhood = [pixel]
        while neighbourhood:
            all_pixels.extend(neighbourhood)
            neighbourhood = self.get_black_neighbourhood(neighbourhood)

        return all_pixels

    def get_black_neighbourhood(self, pixels):
        self.used_pixel.extend(pixels)

        all_neighbourhood = []

        for pixel in pixels:
            neighbourhood = [
                (pixel[0]+1, pixel[1]),
                (pixel[0]-1, pixel[1]),
                (pixel[0], pixel[1]+1),
                (pixel[0], pixel[1]-1)
            ]

            for neighbor in neighbourhood:
                if neighbor[0] < 0 or neighbor[1] < 0:
                    continue

                if neighbor in self.used_pixel:
                    continue

                try:
                    if self.image_arr[neighbor[0]][neighbor[1]] == 255:
                        continue
                except:
                    continue

                all_neighbourhood.append(neighbor)

        return list(set(all_neighbourhood))















    # def _convert_to_numbers(self):
    #     numbers = []
    #     for i, j in itertools.product(range(self.width), range(self.height)):
    #         numbers.extend(self._get_black_neighbourhood((i, j)))
    #     return numbers
    #
    #
    # def _get_black_neighbourhood(self, pixel):
    #     if self.image_arr[pixel[0]][pixel[1]] != 0:
    #         return []
    #
    #     if pixel in self.used_pixel:
    #         return []
    #
    #     print(pixel)
    #
    #     self.used_pixel.append(pixel)
    #     black_neighbourhood = [pixel]
    #
    #     neighbourhood = [
    #         (pixel[0]+1, pixel[1]),
    #         (pixel[0]-1, pixel[1]),
    #         (pixel[0], pixel[1]+1),
    #         (pixel[0], pixel[1]-1)
    #     ]
    #
    #     black_neighbourhood.extend(self._get_black_neighbourhood(neighbourhood[0]))
    #     black_neighbourhood.extend(self._get_black_neighbourhood(neighbourhood[1]))
    #     black_neighbourhood.extend(self._get_black_neighbourhood(neighbourhood[2]))
    #     black_neighbourhood.extend(self._get_black_neighbourhood(neighbourhood[3]))
    #
    #     return black_neighbourhood

if __name__ == '__main__':
    ImageHandler('./images/image_2.png')
