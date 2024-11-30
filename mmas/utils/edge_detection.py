import os
from concurrent.futures import ThreadPoolExecutor

# Reference:
# https://blog.jiayu.co/2019/05/edge-detection-with-imagemagick/

# Requires:
# https://imagemagick.org


def preprocess_image(file_path):
    """
    Convert image to grayscale and remove alpha channel. This creates an intermediate file-format which will make it
    easier for edge detection algorithms to detect changes in color.

    Args:
        file_path (): full path to the image.
    """
    mpc = file_path.replace("png", "mpc")

    # Use imagemagick to convert to grayscale and remove alpha channel.
    os.system(f'magick.exe "{file_path}" -colorspace gray -alpha remove "{mpc}"')


def detect_edges(file_path):
    """
    Perform edge detection on image and output an image with only grain boundaries.

    Args:
        file_path (): full path to the image.
    """
    cache = file_path.replace("png", "cache")
    mpc = file_path.replace("png", "mpc")
    folder_path, file_name = os.path.split(file_path)
    output = os.path.join(
        folder_path, "highlighted-boundaries", file_name.replace(".png", "_edge.png")
    )

    # save output image in 'highlighted-boundaries' folder.
    os.makedirs(os.path.split(output)[0], exist_ok=True)

    preprocess_image(file_path)

    # Use imagemagick to perform edge detection. -auto-threshold Triangle gives the best results for this particular application.
    os.system(
        f'magick.exe "{mpc}" -define morphology:compose=Lighten -morphology Convolve Roberts:@ -negate -auto-threshold Triangle "{output}"'
    )

    # Clean-up intermediate file-formats
    os.remove(mpc)
    os.remove(cache)


def process_microstructures(folder_path):
    print(f"Processing {len(os.listdir(folder_path))} microstructures.")
    with ThreadPoolExecutor() as executor:
        for file in os.listdir(folder_path):
            if not file.endswith(".png") or file.endswith("edge.png"):
                continue

            file_path = os.path.join(folder_path, file)
            executor.submit(detect_edges, file_path)
    print("Completed.")
