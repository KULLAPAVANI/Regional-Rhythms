import os, argparse, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from model import create_sklearn_svc, save_model
from feature_extraction import extract_mfcc, load_hubert_model, extract_hubert_embeddings

def gather_files(data_root):
    items = []
    for label in sorted(os.listdir(data_root)):
        labdir = os.path.join(data_root, label)
        if not os.path.isdir(labdir): continue
        for fn in os.listdir(labdir):
            if fn.lower().endswith(('.wav', '.flac', '.mp3', '.m4a')):
                items.append((os.path.join(labdir, fn), label))
    return items

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data-root', default=os.path.join('..', 'data', 'IndicAccentDb'))
    p.add_argument('--feature', choices=['mfcc','hubert'], default='mfcc')
    p.add_argument('--hubert-model', default='facebook/hubert-base-ls960')
    p.add_argument('--hubert-layer', type=int, default=-1)
    args = p.parse_args()

    items = gather_files(args.data_root)
    if not items:
        print('No audio files found under', args.data_root)
        return
    X=[]; y=[]
    if args.feature=='mfcc':
        for path,label in items:
            try:
                feats = extract_mfcc(path)
                X.append(feats); y.append(label)
            except Exception as e:
                print('mfcc error', path, e)
    else:
        model,processor = load_hubert_model(args.hubert_model)
        for path,label in items:
            try:
                emb = extract_hubert_embeddings(path, model, processor, layer=args.hubert_layer)
                X.append(emb); y.append(label)
            except Exception as e:
                print('hubert error', path, e)
    import numpy as np
    X = np.vstack(X)
    X = X.astype(float)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = create_sklearn_svc()
    clf.fit(X_train, y_train)
    save_model(clf)
    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))

if __name__=='__main__':
    main()
