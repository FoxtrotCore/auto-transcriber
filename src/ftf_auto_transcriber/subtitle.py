from pathlib import Path

from ass import Dialogue, Document

from .utils import get_logger


def build_ass_subtitle(
    audio_path: Path, transcript: dict, transcript_dir: Path
) -> Path:
    LOG = get_logger()

    # Build subtitle name
    subtitle_name = f"{transcript_dir.absolute()}/{audio_path.name.split('.')[0]}.ass"

    # Construct the formatted subtitle
    subtitle = Document()

    for segment in transcript.get("segments"):
        line = Dialogue(
            layer=0,
            start=int(segment.get("start")),
            end=int(segment.get("end")),
            style=f"{segment.get('speaker')}_STYLE",
            name=segment.get("speaker"),
            margin_l=0,
            margin_r=0,
            margin_v=0,
            effect="",
            text=segment.get("text"),
        )
        subtitle.events.append(line)

    # Write to file
    with open(subtitle_name, "w+") as file:
        subtitle.dump_file(file)

    LOG.debug("Saved formatted transcript to file: %s", subtitle_name)
