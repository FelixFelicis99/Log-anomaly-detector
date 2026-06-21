# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn as nn
import numpy as np

app = FastAPI(title="Log Anomaly Detector API")

# Enable CORS so your React frontend can talk to your backend cleanly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Re-declare the model class so PyTorch can safely read the weights structure
class LogAutoencoder(nn.Module):
    def __init__(self, input_dim):
        super(LogAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8)
        )
        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, input_dim)
        )
    def forward(self, x):
        return self.decoder(self.encoder(x))

# Load data and model on startup
X = np.load("features.npy")
input_dim = X.shape[1]

model = LogAutoencoder(input_dim)
model.load_state_dict(torch.load("autoencoder.pth", map_location=torch.device('cpu')))
model.eval()

# Precompute anomaly statistics
X_tensor = torch.FloatTensor(X)
with torch.no_grad():
    predictions = model(X_tensor)
    mse_per_window = torch.mean((X_tensor - predictions) ** 2, dim=1).numpy()

threshold = np.percentile(mse_per_window, 95)

@app.get("/api/anomalies")
def get_anomalies():
    alerts = []
    for idx, mse in enumerate(mse_per_window):
        if mse > threshold:
            # Determine priority tiers based on severity variations
            severity = "CRITICAL" if mse > (threshold * 2) else "WARNING"
            
            alerts.append({
                "window_id": idx,
                "score": float(round(mse, 4)),
                "severity": severity,
                "description": f"Reconstruction error anomaly detected at window row block context {idx}."
            })
            
    return {
        "total_checked_windows": len(mse_per_window),
        "total_anomalies": len(alerts),
        "threshold": float(round(threshold, 4)),
        "anomalies": alerts
    }