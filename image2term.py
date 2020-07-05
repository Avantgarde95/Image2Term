import sys
from PIL import Image

class Image2Term(object):
    def __init__(self, path):
        self.image = Image.open(path).convert('RGB')
        self.width, self.height = self.image.size

    def generate(self, height_new, message):
        # resize the image
        width_new = int((self.width * height_new) / self.height)
        image_new = self.image.resize((width_new, height_new), Image.ANTIALIAS)
        pixels_new = image_new.load()

        # generate ANSI escape codes
        len_message = len(message)
        codes = [[''] * width_new for i in range(height_new)]

        for i in range(height_new):
            for j in range(width_new):
                r, g, b = pixels_new[j, i]
                index_message = (j % int(len_message / 2)) * 2

                codes[i][j] = '\033[38;2;%d;%d;%dm%s%s' % (
                        r, g, b,
                        message[index_message], message[index_message + 1]
                )

        # pack the codes
        result = '\n'.join(
            ''.join(codes[i][j] for j in range(width_new))
            for i in range(height_new)
        )

        # restore the original settings
        result += '\033[0m'

        return result

def main():
    if len(sys.argv) < 4:
        print(
                'Usage: %s path height message\n' \
                'ex. %s MonaLisa.png 40 MONALISA\n' \
                '- path: Path of your image\n'
                '- height: Height of the result (in characters)\n'
                '- message: String which will be printed on the result'
                % (sys.argv[0], sys.argv[0])
        )

        return

    path = sys.argv[1]
    height = int(sys.argv[2])
    message = sys.argv[3] * 2 # make the length even

    print(Image2Term(path).generate(height, message))

main()

