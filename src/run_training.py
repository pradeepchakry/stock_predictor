import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
from src.data.load_data import load_stock_data
import matplotlib.pyplot as plt

def create_dataset(dataset, time_steps=60):
    X, y = [], []
    for i in range(time_steps, len(dataset)):
        X.append(dataset[i - time_steps:i, 0])
        y.append(dataset[i, 0])
    return np.array(X), np.array(y)

def plot_predictions(model, X_test, y_test, scaler, close_prices):
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)
    actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

    plt.figure(figsize=(10, 6))
    plt.plot(actual_prices, color='green', label='Actual Price')
    plt.plot(predictions, color='red', label='Predicted Price')
    plt.title('Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

def main():
    scaled_data, scaler, close_prices = load_stock_data("AAPL", "2020-01-01", "2025-01-01")

    time_steps = 60
    X, y = create_dataset(scaled_data, time_steps)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
        LSTM(50, return_sequences=False),
        Dense(25),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=5, batch_size=32)

    plot_predictions(model, X_test, y_test, scaler, close_prices)

if __name__ == "__main__":
    main()
