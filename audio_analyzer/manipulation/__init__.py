import os, logging, speech_recognition as sr, time, json, pickle
from pathlib import Path
from ffmpeg import FFmpeg

Audio = tuple[Path, sr.AudioData, int]
Speech = tuple[Path, str]

logger = logging.getLogger(__name__)


def convert_video(sources: Path, out: Path) -> list[Path]:
    logger.info("Converting videos to audio...")
    outs: list[Path] = []
    out.mkdir(parents=True, exist_ok=True)

    for input in os.listdir(sources):
        if input == ".gitkeep":
            continue

        input = Path(input)
        outs.append(out / input.with_suffix(".wav"))
        if outs[-1].exists():
            continue

        print(sources / input)
        print(outs[-1])

        FFmpeg().option("y").input(sources / input).output(outs[-1]).execute()

    logger.info("Videos converted, or already converted and skipping.")
    return outs


def paths_to_audio(r: sr.Recognizer, tracks: list[Path], cache: Path) -> list[Audio]:
    logger.info("Converting tracks to audio data...")
    cache = Path(cache)
    if cache.exists():
        with cache.open("rb") as f:
            outs = pickle.load(f)
        logger.info("Got audio data from cache.")
        return outs

    outs = []

    for track in tracks:
        with sr.AudioFile(str(track)) as source:
            outs.append((Path(track), r.record(source), source.DURATION))

    with cache.open("wb") as f:
        pickle.dump(outs, f)

    logger.info("Converted to audio data successfully.")
    return outs


def audio_to_speeches(
    *,
    r: sr.Recognizer,
    lang: str,
    audio: list[Audio],
    out: Path,
) -> list[Speech]:
    logger.info("Converting the tracks to text...")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)

    res, recognition_time = [], 0
    already_converted = 0

    for path, data, _ in audio:
        output = Path(out / path.with_suffix(".txt").name)

        if output.exists():
            already_converted += 1
            with output.open() as f:
                res.append((path, f.read()))
            continue

        try:
            logger.info(f"Recognizing speech for {path}")

            start = time.time()
            text = r.recognize_vosk(data, language=lang)
            recognition_time += time.time() - start

            actual_text = json.loads(text)["text"]

            logger.info("Recognized. Writing to file...")

            res.append((path, actual_text))
            with output.open("w+") as f:
                f.write(actual_text)
        except sr.UnknownValueError:
            logger.error(f"VOSK could not understand audio {path}")
        except Exception as e:
            logger.error(f"Error: {e}", stack_info=True)

    if already_converted != 0:
        logger.info(f"Already converted files: {already_converted}")

    logger.info("Tracks converted.")
    return res
