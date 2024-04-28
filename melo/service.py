# WebUI by mrfakename <X @realmrfakename / HF @mrfakename>
# Demo also available on HF Spaces: https://huggingface.co/spaces/mrfakename/MeloTTS
import os, torch, io
# os.system('python -m unidic download')
from flask import Flask, Response,request
print("Make sure you've downloaded unidic (python -m unidic download) for this WebUI to work.")
from melo.api import TTS
speed = 1.0
import tempfile
import click
device = 'auto'
models = {
    'EN': TTS(language='EN', device=device),
    'ES': TTS(language='ES', device=device),
    'FR': TTS(language='FR', device=device),
    'ZH': TTS(language='ZH', device=device),
    'JP': TTS(language='JP', device=device),
    'KR': TTS(language='KR', device=device),
}
speaker_ids = models['EN'].hps.data.spk2id

default_text_dict = {
    'EN': 'The field of text-to-speech has seen rapid development recently.',
    'ES': 'El campo de la conversión de texto a voz ha experimentado un rápido desarrollo recientemente.',
    'FR': 'Le domaine de la synthèse vocale a connu un développement rapide récemment',
    'ZH': 'text-to-speech 领域近年来发展迅速',
    'JP': 'テキスト読み上げの分野は最近急速な発展を遂げています',
    'KR': '최근 텍스트 음성 변환 분야가 급속도로 발전하고 있습니다.',    
}
app = Flask(__name__)

@app.route('/api/speek')
def speek():
     texts = request.form.get("texts")
     response = Response()
     if texts != "":
         response.headers['Content-Type'] = 'audio/wav'
         audio = synthesize("ZH", texts, 1, "ZH")
         response.stream.write(audio)
         return response
     else:
        return Response(status=404)



def synthesize(speaker, text, speed, language):
    bio = io.BytesIO()
    models[language].tts_to_file(text, models[language].hps.data.spk2id[speaker], bio, speed=speed, pbar=None, format='wav')
    return bio.getvalue()



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=9010)
