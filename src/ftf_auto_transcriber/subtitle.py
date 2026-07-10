from json import dump
from pathlib import Path

from ass import Dialogue, Document

from .utils import get_logger


def build_ass_subtitle(audio_path: Path, transcript: list[dict]) -> Path:
    LOG = get_logger()

    # Build subtitle name
    subtitle_name = f"{audio_path.name.split('.')[0]}.ass"
    json_name = f"{audio_path.name.split('.')[0]}.json"
    subtitle_path = audio_path.parent.joinpath(subtitle_name)
    with open(json_name, "w+") as file:
        dump(transcript, file)

    # Construct the formatted subtitle
    subtitle = Document()

    for segment in transcript:
        line = Dialogue(
            layer=0,
            start=int(segment.get("start")),
            end=int(segment.get("end")),
            style="ACTOR_STYLE",
            name="ACTOR",
            margin_l=0,
            margin_r=0,
            margin_v=0,
            effect="",
            text=segment.get("text"),
        )
        subtitle.events.append(line)

    # Write to file
    with open(subtitle_path, "w+") as file:
        subtitle.dump_file(file)

    LOG.debug("Saved formatted transcript to file: %s", subtitle_path)
