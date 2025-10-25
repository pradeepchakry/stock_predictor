import numpy as np
from sklearn.preprocessing import MinMaxScaler

def create_sequences(data, seq_len=60):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(seq_len, len(scaled_data)):
        X.append(scaled_data[i - seq_len:i, 0])
        y.append(scaled_data[i, 0])

    X = np.array(X)
    y = np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    split = int(len(X) * 0.8)
    return X[:split], y[:split], X[split:], y[split:], scaler, data
