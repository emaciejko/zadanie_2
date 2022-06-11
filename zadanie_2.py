from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/UG_encode.png"):
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            if bin(red_channel.getpixel((i, j)))[-1] == '0':
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0,0,0)

    decoded_image.save("images/UG_decode.png")

def write_text(text_to_write, image_size):
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="images/UG.jpg"):
    img = Image.open(template_image)
    red_img = img.split()[0]
    green_img = img.split()[1]
    blue_img = img.split()[2]
    x = img.size[0]
    y = img.size[1]
    coded_image = Image.new("RGB", (x, y))
    image_text = write_text(text_to_encode, img.size)
    bw_encode = image_text.convert('1')
    pixels = coded_image.load()

    for i in range(x):
        for j in range(y):
            red_pix = bin(red_img.getpixel((i,j)))
            pix = bin(bw_encode.getpixel((i,j)))

            if pix[-1] == '1':
                red_pix = red_pix[:-1] + '1'
            else:
                red_pix = red_pix[:-1] + '0'
            pixels[i, j] = (int(red_pix, 2), green_img.getpixel((i,j)), blue_img.getpixel((i,j)))

    coded_image.save("images/UG_coded.jpg")

if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    print("Encoding the image...")
    encode_image()