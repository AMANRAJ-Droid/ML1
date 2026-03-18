import numpy as np

def compute_uncertainty(probs, threshold=0.5):
    confidence = np.max(probs, axis=1)
    uncertain_flag = (confidence < threshold).astype(int)
    return confidence, uncertain_flag