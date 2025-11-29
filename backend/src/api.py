"""Flask API for prediction with MFCC + HuBERT support and cuisine mapping."""
import os, tempfile, json
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from feature_extraction import extract_mfcc, load_hubert_model, extract_hubert_embeddings
from model import load_model
app = Flask(__name__)
ALLOWED = ('.wav','.flac','.mp3','.m4a')
CUISINE_MAP = {
    'Malayalam': ['Appam','Puttu','Avial'],
    'Tamil': ['Dosa','Idli','Pongal'],
    'Telugu': ['Hyderabadi Biryani','Pesarattu','Gongura Pickle'],
    'Hindi': ['Chole Bhature','Aloo Paratha','Rajma'],
    'Punjabi': ['Butter Chicken','Amritsari Kulcha','Sarson ka Saag'],
    'Bengali': ['Fish Curry','Rosogolla','Mishti Doi']
}
MODEL=None

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

@app.route('/predict', methods=['POST'])
def predict():
    global MODEL
    feat_type = request.form.get('feature','mfcc')
    hubert_layer = int(request.form.get('hubert_layer', -1))
    if 'file' not in request.files:
        return jsonify({'error':'no file'}),400
    f = request.files['file']
    if f.filename=='':
        return jsonify({'error':'no filename'}),400
    fn = secure_filename(f.filename)
    ext = os.path.splitext(fn)[1].lower()
    if ext not in ALLOWED:
        return jsonify({'error':'unsupported'}),400
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    f.save(tmp.name)
    try:
        if feat_type=='mfcc':
            feats = extract_mfcc(tmp.name)
        else:
            model_h, proc = load_hubert_model()
            feats = extract_hubert_embeddings(tmp.name, model_h, proc, layer=hubert_layer)
        if MODEL is None:
            MODEL = load_model()
        probs = MODEL.predict_proba([feats])[0].tolist()
        pred = MODEL.predict([feats])[0]
        classes = MODEL.classes_.tolist()
        cuisine = []
        for k,v in CUISINE_MAP.items():
            if k.lower() in pred.lower() or pred.lower() in k.lower():
                cuisine = v; break
        if not cuisine:
            top = classes[probs.index(max(probs))]
            for k,v in CUISINE_MAP.items():
                if k.lower() in top.lower():
                    cuisine=v; break
        return jsonify({'prediction':pred,'classes':classes,'probabilities':probs,'recommended_cuisines':cuisine})
    except Exception as e:
        return jsonify({'error':str(e)}),500
    finally:
        try:
            os.unlink(tmp.name)
        except: pass

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
