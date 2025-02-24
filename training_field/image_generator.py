from random import randint, choices
from PIL import Image
from darken_image import random_darkening

def check_overlap(x1, y1, w1, h1, x2, y2, w2, h2):
    e = 6 # Increase this value for more overlap of droplets
    return (x2 + e < x1 + w1 and x1 < x2 + w2 - e) and (y2 + e < y1 + h1 and y1 < y2 + h2 - e)

def place_images(big_image_path, small_images_path, num_small_images, output_image_path, output_labels_path):
    darken = choices(["background", "final", "none"], weights=[0.3, 0.3, 0.4], k=1)[0]
    big_image = Image.open(big_image_path)
    if darken == "background":
        big_image = random_darkening(big_image)

    current_width, current_height = big_image.size
    desired_size = 640
    left = (current_width - desired_size) / 2
    top = (current_height - desired_size) / 2
    right = (current_width + desired_size) / 2
    bottom = (current_height + desired_size) / 2
    big_image = big_image.crop((left, top, right, bottom))

    small_images = [Image.open(i) for i in small_images_path]

    big_width, big_height = big_image.size
    smalls_dimentions = [i.size for i in small_images]

    labels = []
    positions = []

    combined_image = big_image.copy()

    max_attempts = 25
    placed = too_many_failed = 0
    while placed < num_small_images and too_many_failed < 20:
        chosen_small = randint(0, len(small_images)-1)
        small_image = small_images[chosen_small]
        small_width, small_height = smalls_dimentions[chosen_small]

        attempts = 0
        while attempts < max_attempts and placed < num_small_images:
            x = randint(0, big_width-small_width)
            y = randint(0, big_height-small_height)

            overlap = False
            for (px, py, pwidth, pheight) in positions:
                if check_overlap(x, y, small_width, small_height, px, py, pwidth, pheight):
                    overlap = True
                    break

            if not overlap:
                combined_image.paste(small_image, (x, y), small_image)

                x_center = (x + small_width / 2) / big_width
                y_center = (y + small_height / 2) / big_height
                width = small_width / big_width
                height = small_height / big_height

                labels.append(f"0 {x_center} {y_center} {width} {height}")
                positions.append((x, y, small_width, small_height))
                placed += 1
            else:
                attempts += 1
        if attempts == max_attempts:
            too_many_failed += 1

    if darken == "final":
        combined_image = random_darkening(combined_image)

    combined_image.save(output_image_path)

    with open(output_labels_path, 'w') as f:
        for label in labels:
            f.write(f"{label}\n")