import matplotlib.pyplot as plt
import encodemaptoimage as emi

def main():
    # Load audio file and return as a tensor
    path = "./Nexta/LNexta.osu"
    print(path)

    img = emi.encode_map_to_image(path, 500, 630)

    plt.imshow(img, cmap='gray')
    plt.show()


if __name__ == "__main__":
    main()
