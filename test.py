from lightning_whisper_mlx import LightningWhisperMLX

whisper = LightningWhisperMLX(model="distil-medium.en", batch_size=12, quant=None)

text = whisper.transcribe(audio_path="downloads/audio/28 😱 CURIOSIDADES SOBRE 😲 LA SERIE SENNA #142｜Detrasdelguion.mp3")['text']

print(text)