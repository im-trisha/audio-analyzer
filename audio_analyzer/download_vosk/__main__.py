import os, requests, zipfile, argparse, logging
from audio_analyzer.utils import K_LOGGER_FORMAT, K_MODELS_PATH
from pathlib import Path
from tqdm import tqdm


logging.basicConfig(format=K_LOGGER_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


def download_vosk_model(model_name):
    url = f"https://alphacephei.com/vosk/models/{model_name}.zip"

    K_MODELS_PATH.mkdir(exist_ok=True)
    zip_path = K_MODELS_PATH / f"{model_name}.zip"

    # Stream download with progress bar
    logger.info(f"Downloading model '{model_name}' from {url}...")
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Ensure the request was successful
        total_size = int(response.headers.get("content-length", 0))
        with open(zip_path, "wb") as file, tqdm(
            desc=str(zip_path),
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                progress_bar.update(len(data))

    # Extract the model
    logger.info(f"Extracting '{model_name}' to {K_MODELS_PATH}...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(K_MODELS_PATH)

    os.remove(zip_path)
    logger.info(f"Model '{model_name}' downloaded and extracted to {K_MODELS_PATH}.")


def main():
    parser = argparse.ArgumentParser(description="Download and extract a VOSK model.")
    parser.add_argument(
        "model_name", type=str, help="The name of the VOSK model to download"
    )
    args = parser.parse_args()

    download_vosk_model(args.model_name)


if __name__ == "__main__":
    main()
