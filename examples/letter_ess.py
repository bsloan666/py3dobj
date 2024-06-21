import font
import objio

if __name__ == "__main__":

    points, indices = font.letter_s(20, 7)

    objio.save("./letter_s.obj", points, indices)
