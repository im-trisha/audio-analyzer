import logging, argparse
from pathlib import Path


K_MODELS_PATH = Path("models/")

K_SOURCES, K_AUDIOOUT, K_CACHEDATA, K_SPEECHOUT = (
    Path("./data/sources"),
    Path("./data/cache/audio"),
    Path("./data/cache/audiodata.pickle"),
    Path("./data/cache/speeches"),
)
K_VOSK_MODEL, K_LANG = "vosk-model-it-0.22", "it"
K_INVALIDATE_CACHE = False
K_LOGGER_FORMAT = "[%(asctime)s] %(name)s:%(lineno)d %(levelname)s - %(message)s"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process videos and search text inside them"
    )
    parser.add_argument(
        "--sources",
        default=K_SOURCES,
        type=Path,
        help="Path to the video sources folder.",
    )
    parser.add_argument(
        "--audio-cache",
        default=K_AUDIOOUT,
        type=Path,
        help="Path to save cached audio",
    )
    parser.add_argument(
        "--cache-data",
        default=K_CACHEDATA,
        type=Path,
        help="Path to the cache audio data file.",
    )
    parser.add_argument(
        "--speech-cache",
        default=K_SPEECHOUT,
        type=Path,
        help="Path to save speech recognition output.",
    )
    parser.add_argument(
        "--vosk-model",
        default=K_VOSK_MODEL,
        help=f"Name of the VOSK model. Must be placed inside {K_MODELS_PATH}",
    )
    parser.add_argument(
        "--language",
        default=K_LANG,
        help="Language for speech recognition.",
    )
    parser.add_argument(
        "--invalidate-cache",
        action="store_true",
        default=K_INVALIDATE_CACHE,
        help="Invalidate cache if specified.",
    )

    parser.add_argument(
        "-s",
        nargs="*",
        required=True,
        type=str.lower,
        help="List of keywords to search for in audio.",
    )

    return parser.parse_args()
