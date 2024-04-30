
import io, os
import hashlib
from flask import Flask, Response, request
from melo.api import TTS
speed = 1.0
device = 'auto'
models = {
    'ZH': TTS(language='ZH', device=device,ckpt_path='./model/zh/checkpoint.pth',config_path='./model/zh/config.json'),
}
speaker_ids = models['ZH'].hps.data.spk2id
cache_dir = "/data/chache/"
default_text_dict = {
    'EN': 'The field of text-to-speech has seen rapid development recently.',
    'ES': 'El campo de la conversión de texto a voz ha experimentado un rápido desarrollo recientemente.',
    'FR': 'Le domaine de la synthèse vocale a connu un développement rapide récemment',
    'ZH': 'text-to-speech 领域近年来发展迅速',
    'JP': 'テキスト読み上げの分野は最近急速な発展を遂げています',
    'KR': '최근 텍스트 음성 변환 분야가 급속도로 발전하고 있습니다.',    
}
app = Flask(__name__)

def generate_md5(text):
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode('utf-8'))
    return md5_hash.hexdigest()

@app.route('/api/speechSynthesis',methods=['POST'])
def speechSynthesis():
        texts = request.form.get("texts")
        hashCode = generate_md5(texts)
        response = Response()
        response.headers['Content-Type'] = 'audio/wav'
        cacheFile = os.path.join(cache_dir, hashCode + '.wav')
        if os.path.exists(cacheFile):
            with open(cacheFile) as f:
                chunk_size = 1024
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    response.stream.write(chunk)

        if texts != "":
            audio = synthesize("ZH", texts, 1, "ZH")
            with open(cacheFile) as f:
                f.write(audio)
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
