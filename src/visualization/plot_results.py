import matplotlib.pyplot as plt

def plot_predictions(model, X_test, y_test, scaler, data):
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)
    true_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

    plt.figure(figsize=(12, 6))
    plt.plot(true_prices, label='Actual Prices')
    plt.plot(predictions, label='Predicted Prices')
    plt.title('Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
