"""Feature extraction module supporting MFCCs and HuBERT embeddings.
Functions:
- extract_mfcc(path)
- extract_hubert_embeddings(path, model, processor, layer=-1)
- helper to load HuBERT model and processor
"""
import numpy as np
import librosa
import soundfile as sf

def extract_mfcc(path, sr=16000, n_mfcc=13):
    y, sr = librosa.load(path, sr=sr)
    y, _ = librosa.effects.trim(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    mfcc_mean = mfcc.mean(axis=1)
    mfcc_std = mfcc.std(axis=1)
    features = np.concatenate([mfcc_mean, mfcc_std])
    return features

def load_hubert_model(name='facebook/hubert-base-ls960'):
    from transformers import AutoModel, AutoFeatureExtractor
    import torch
    model = AutoModel.from_pretrained(name, output_hidden_states=True)
    processor = AutoFeatureExtractor.from_pretrained(name)
    model.eval()
    return model, processor

def extract_hubert_embeddings(path, model, processor, layer=-1, target_sr=16000):
    import torch
    import soundfile as sf
    wav, sr = sf.read(path)
    if sr != target_sr:
        import librosa
        wav = librosa.resample(wav.astype(float), orig_sr=sr, target_sr=target_sr)
    inputs = processor(wav, sampling_rate=target_sr, return_tensors='pt', padding=True)
    with torch.no_grad():
        out = model(**inputs, output_hidden_states=True)
    hidden_states = out.hidden_states
    chosen = hidden_states[layer]
    emb = chosen.mean(dim=1).squeeze().cpu().numpy()
    return emb
