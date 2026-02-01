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


def predict_one(feature_predict):
 bundle = load_bundle()
 model = bundle["model"]
 order = bundle["feature_cols"]

 # Build input array
 X = [[float(feature_predict[c]) for c in order]]

 # Predict
 pred = model.predict(X)

 # Convert to string if needed
 if isinstance(pred, (list, tuple, np.ndarray)):
    pred = pred[0]  # take first element

 return str(pred)

