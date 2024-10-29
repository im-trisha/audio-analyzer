import logging
from datetime import timedelta
from audio_analyzer.manipulation import Speech, Audio

logger = logging.getLogger(__name__)


def search_speeches(
    speeches: list[Speech],
    audio: list[Audio],
    needles: list[str],
) -> None:
    logger.info("Finding needle in haystack...")
    for i, (path, haystack) in enumerate(speeches):
        haystack_len = len(haystack)
        for needle in needles:
            pos = haystack.find(needle)
            if pos > -1:
                pos_percent = (pos / haystack_len) * 100
                pos_duration = timedelta(seconds=audio[i][2] * (pos / haystack_len))

                logger.info(
                    f"Found {needle} in {path.with_suffix('').name}, approx. position: {pos_percent:.2f}%, approx. time: {pos_duration}"
                )
    logger.info("Finished. Goodbye")
