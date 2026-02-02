import os
import pickle
from functools import lru_cache
from django.conf import  settings
import numpy as np 
@lru_cache(maxsize=1)
def load_bundle():
     pkl_path=os.path.join(settings.BASE_DIR,'crop_app','ml','Crop_recomentation.pkl')
     with open(pkl_path,'rb') as f:
        bundle=pickle.load(f)
  
     assert "model" in bundle and 'feature_cols' in bundle, "invalid model bundle structure"
     return bundle


def predict_one(feature_predict, top_n=3):
 bundle = load_bundle()
 model = bundle["model"]
 order = bundle["feature_cols"]

 # Build input array in correct order
 X = [[float(feature_predict[c]) for c in order]]

 # Get probability for each class
 probs = model.predict_proba(X)[0]  # list of probabilities per class
 classes = model.classes_           # list of class names

 # Zip class names and probabilities
 crop_probs = list(zip(classes, probs))

 # Sort descending by probability
 crop_probs.sort(key=lambda x: x[1], reverse=True)

 # Take top N crops
 top_crops = [c[0] for c in crop_probs[:top_n]]

 return top_crops
