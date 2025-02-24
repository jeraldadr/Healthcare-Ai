from transformers import pipeline
import torch
import sys
from transformers.pipelines.audio_utils import ffmpeg_microphone_live
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

device = "cuda:0" if torch.cuda.is_available() else "cpu"

#PREPROCESSING


classifier = pipeline(
    "audio-classification", model="MIT/ast-finetuned-speech-commands-v2", device=device
)

transcriber = pipeline(
    "automatic-speech-recognition", model="openai/whisper-small.en", device=device
)

def launch_fn(
    wake_word="marvin",
    prob_threshold=0.5,
    chunk_length_s=2.0,
    stream_chunk_s=0.25,
    debug=False,
):
    if wake_word not in classifier.model.config.label2id.keys():
        raise ValueError(
            f"Wake word {wake_word} not in set of valid class labels, pick a wake word in the set {classifier.model.config.label2id.keys()}."
        )

    sampling_rate = classifier.feature_extractor.sampling_rate

    mic = ffmpeg_microphone_live(
        sampling_rate=sampling_rate,
        chunk_length_s=chunk_length_s,
        stream_chunk_s=stream_chunk_s,
    )

    print("Listening for wake word...")
    for prediction in classifier(mic):
        prediction = prediction[0]
        if debug:
            print(prediction)
        if prediction["label"] == wake_word:
            if prediction["score"] > prob_threshold:
                tts("How can I help you?")
                return True



def transcribe(chunk_length_s=2.0, stream_chunk_s=0.5):
    sampling_rate = transcriber.feature_extractor.sampling_rate
    mic = ffmpeg_microphone_live(
        sampling_rate=sampling_rate,
        chunk_length_s=chunk_length_s,
        stream_chunk_s=stream_chunk_s,
    )

    print("Start speaking...")
    for item in transcriber(mic, generate_kwargs={"max_new_tokens": 128}):
        sys.stdout.write("\033[K")
        print(item["text"], end="\r")
        if not item["partial"][0]:
            break

    return item["text"]


def tts(prompt):
    load_dotenv()

    client = ElevenLabs()

    audio = client.text_to_speech.convert(
        text=prompt,
        voice_id="pPdl9cQBQq4p6mRkZy2Z",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    play(audio)




if __name__ == '__main__':
    launch_fn()
    transcription = transcribe()
    response = query(transcription)

    audio = tts(response)

