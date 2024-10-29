import logging, speech_recognition as sr
from vosk import Model
from audio_analyzer.manipulation import convert_video, paths_to_audio, audio_to_speeches
from audio_analyzer.search import search_speeches
from audio_analyzer.utils import parse_args, K_LOGGER_FORMAT, K_MODELS_PATH

logging.basicConfig(format=K_LOGGER_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:

    args = parse_args()

    logger.info("Initializing VOSK model...")
    r = sr.Recognizer()
    r.vosk_model = Model(str(K_MODELS_PATH / args.vosk_model))
    logger.info("VOSK model initialized.")

    tracks = convert_video(args.sources, args.audio_cache)

    audio = paths_to_audio(r, tracks, args.cache_data)

    speeches = audio_to_speeches(
        r=r,
        lang=args.language,
        audio=audio,
        out=args.speech_cache,
    )

    search_speeches(speeches, audio, args.s)


if __name__ == "__main__":
    main()
