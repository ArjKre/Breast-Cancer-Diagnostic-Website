from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image

dataset = Path("../dataset")

images = list((dataset / "benign").glob("*"))[:4]

plt.figure(figsize=(10, 10))

for i, image_path in enumerate(images):
    img = Image.open(image_path)

    plt.subplot(2, 2, i + 1)

    plt.imshow(img, cmap="gray")

    plt.axis("off")

plt.savefig("./output.png")
