from json import dump, load
from pathlib import Path

from whisperx import assign_word_speakers, load_audio, load_model
from whisperx.SubtitlesProcessor import SubtitlesProcessor

from .utils import get_logger


def dump_raw_transcript(
    audio_path: Path, transcript_dir: Path, transcript: dict
) -> Path:
    LOG = get_logger()

    # Build transcript name
    transcript_name = f"{audio_path.name.split('.')[0]}.json"
    transcript_path = transcript_dir.joinpath(transcript_name)

    # Write to file
    with open(transcript_path.absolute(), "w+") as file:
        dump(
            transcript,
            file,
            ensure_ascii=False,
            indent=4,
            sort_keys=True,
            check_circular=True,
        )

    LOG.debug("Saved raw transcript to file: %s", transcript_path)
    return transcript_path


def transcribe(
    audio_path: Path,
    transcript_dir: Path,
    device: str,
    model: str,
    language: str,
    batch_size: int,
    compute_type: str,
    diarize: bool,
    min_speakers: int,
    max_speakers: int,
) -> SubtitlesProcessor:
    LOG = get_logger()

    # Build transcript name
    transcript_name = f"{audio_path.name.split('.')[0]}.json"
    transcript_path = transcript_dir.joinpath(transcript_name)

    # Check if transcript has already been done
    if transcript_path.exists():
        LOG.warning(
            "Transcription file already exists! Loading from: %s",
            transcript_path.absolute(),
        )
        with open(transcript_path.absolute(), "r") as file:
            raw_transcript: dict = load(file)
            return SubtitlesProcessor(
                segments=raw_transcript.get("segments"),
                lang=language,
                max_line_length=80,
                min_char_length_splitter=32,
            )

    # Load audio file
    audio = load_audio(audio_path)

    # Load ASR model
    LOG.debug("Downloading ASR model: %s", model)
    asr_model = load_model(
        model, device=device, compute_type=compute_type, language=language
    )

    LOG.debug(
        "Transcribing %s with params: (device: %s, model: %s, language: %s, batch size: %s, compute type: %s, diarize: %s)",
        audio_path,
        device,
        model,
        language,
        batch_size,
        compute_type,
        diarize,
    )
    raw_transcript: dict = asr_model.transcribe(audio, language=language)

    return SubtitlesProcessor(
        segments=raw_transcript.get("segments"),
        lang=language,
        max_line_length=80,
        min_char_length_splitter=32,
    )
