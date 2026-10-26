"""Generate clean full-page background gradient descent 3D visual with stick arrow (──►)."""

import json
import numpy as np
from sklearn.datasets import make_moons

np.random.seed(42)

# Generate dataset
X, Y = make_moons(n_samples=250, noise=0.25, random_state=42)
Y = Y.reshape(-1, 1)

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros((1, output_size))

    def forward(self, X):
        self.Z1 = np.dot(X, self.W1) + self.b1
        self.A1 = self.sigmoid(self.Z1)
        self.Z2 = np.dot(self.A1, self.W2) + self.b2
        self.A2 = self.sigmoid(self.Z2)
        return self.A2

    def backward(self, X, Y, output):
        m = Y.shape[0]
        dZ2 = output - Y
        dW2 = np.dot(self.A1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m
        dZ1 = np.dot(dZ2, self.W2.T) * (self.A1 * (1 - self.A1))
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        return dW1, db1, dW2, db2

    def update_parameters(self, dW1, db1, dW2, db2, learning_rate):
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2

    def sigmoid(self, Z):
        return 1.0 / (1.0 + np.exp(-np.clip(Z, -250, 250)))

nn = NeuralNetwork(input_size=2, hidden_size=10, output_size=1)
steps = []
learning_rate = 0.35
num_epochs = 200

for epoch in range(num_epochs):
    out = nn.forward(X)
    loss = float(np.mean((out - Y) ** 2))
    acc = float(np.mean((out > 0.5) == Y))
    
    dW1, db1, dW2, db2 = nn.backward(X, Y, out)
    
    w1_norm = float(np.linalg.norm(nn.W1))
    w2_norm = float(np.linalg.norm(nn.W2))
    dw1_norm = float(np.linalg.norm(dW1))
    dw2_norm = float(np.linalg.norm(dW2))
    
    steps.append({
        "epoch": epoch,
        "w1": round(w1_norm, 4),
        "w2": round(w2_norm, 4),
        "loss": round(loss, 5),
        "acc": round(acc * 100, 1),
        "dw1": round(dw1_norm, 5),
        "dw2": round(dw2_norm, 5)
    })
    
    nn.update_parameters(dW1, db1, dW2, db2, learning_rate=learning_rate)

print(f"Generated {len(steps)} steps of training.")

# Full-page ambient 3D background visual without text/hud overlays
bg_html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>3D Background</title>
<script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
<style>
* { box-sizing: border-box; }
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background: transparent;
  overflow: hidden;
}
#plot {
  width: 100%;
  height: 100%;
  pointer-events: none;
}
</style>
</head>
<body>
<div id="plot"></div>

<script>
const data = DATA_PLACEHOLDER;
let currentEpoch = 0;
let showGradient = false;

const w1_vals = data.map(d => d.w1);
const w2_vals = data.map(d => d.w2);
const loss_vals = data.map(d => d.loss);

const minW1 = Math.min(...w1_vals) - 0.2, maxW1 = Math.max(...w1_vals) + 0.2;
const minW2 = Math.min(...w2_vals) - 0.2, maxW2 = Math.max(...w2_vals) + 0.2;
const minLoss = Math.min(...loss_vals) - 0.05, maxLoss = Math.max(...loss_vals) + 0.05;

// Reference 3D surface
const surfaceX = [], surfaceY = [], surfaceZ = [];
const gridSteps = 24;
for (let i = 0; i <= gridSteps; i++) surfaceX.push(minW1 + (maxW1 - minW1) * (i / gridSteps));
for (let j = 0; j <= gridSteps; j++) surfaceY.push(minW2 + (maxW2 - minW2) * (j / gridSteps));
for (let j = 0; j <= gridSteps; j++) {
  const row = [];
  const y = surfaceY[j];
  for (let i = 0; i <= gridSteps; i++) {
    const x = surfaceX[i];
    const dX = (x - maxW1);
    const dY = (y - maxW2);
    const z = minLoss + 0.2 * (dX * dX + dY * dY * 0.4);
    row.push(z);
  }
  surfaceZ.push(row);
}

const surfaceTrace = {
  type: 'surface',
  x: surfaceX,
  y: surfaceY,
  z: surfaceZ,
  opacity: 0.25,
  showscale: false,
  colorscale: 'Blues',
  hoverinfo: 'none'
};

const pathTrace = {
  type: 'scatter3d',
  mode: 'lines',
  x: [w1_vals[0]],
  y: [w2_vals[0]],
  z: [loss_vals[0]],
  line: { color: '#7fe1d6', width: 5 },
  hoverinfo: 'none'
};

const pointTrace = {
  type: 'scatter3d',
  mode: 'markers',
  x: [w1_vals[0]],
  y: [w2_vals[0]],
  z: [loss_vals[0]],
  marker: { size: 7, color: '#bcf587', line: { color: '#ffffff', width: 2 } },
  hoverinfo: 'none'
};

// 3D Arrow (──►)
const arrowTrace = {
  type: 'scatter3d',
  mode: 'lines',
  x: [null],
  y: [null],
  z: [null],
  line: { color: '#ff3366', width: 8 },
  hoverinfo: 'none'
};

const layout = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor: 'rgba(0,0,0,0)',
  margin: { l: 0, r: 0, b: 0, t: 0 },
  scene: {
    xaxis: { showgrid: true, gridcolor: 'rgba(44, 53, 68, 0.4)', showticklabels: false, title: '', range: [minW1, maxW1], zerolinecolor: 'rgba(44,53,68,0.5)' },
    yaxis: { showgrid: true, gridcolor: 'rgba(44, 53, 68, 0.4)', showticklabels: false, title: '', range: [minW2, maxW2], zerolinecolor: 'rgba(44,53,68,0.5)' },
    zaxis: { showgrid: true, gridcolor: 'rgba(44, 53, 68, 0.4)', showticklabels: false, title: '', range: [minLoss, maxLoss], zerolinecolor: 'rgba(44,53,68,0.5)' },
    camera: { eye: { x: 1.45, y: -1.65, z: 1.15 } }
  },
  showlegend: false
};

Plotly.newPlot('plot', [surfaceTrace, pathTrace, pointTrace, arrowTrace], layout, { responsive: true, displayModeBar: false });

function computeStickArrow(x0, y0, z0, x1, y1, z1) {
  const rx = maxW1 - minW1, ry = maxW2 - minW2, rz = maxLoss - minLoss;
  const dx = x1 - x0, dy = y1 - y0, dz = z1 - z0;
  const nx = dx / rx, ny = dy / ry, nz = dz / rz;
  const nlen = Math.sqrt(nx*nx + ny*ny + nz*nz);
  if (nlen < 1e-6) return { x: [null], y: [null], z: [null] };

  const L = 0.32;
  const ux = (nx / nlen) * rx * L;
  const uy = (ny / nlen) * ry * L;
  const uz = (nz / nlen) * rz * L;

  const tipX = x0 + ux;
  const tipY = y0 + uy;
  const tipZ = z0 + uz;

  // Barbs pointing back like ->
  const barbFrac = 0.38;
  const spread = 0.25;
  
  let px = -uy/ry, py = ux/rx;
  const plen = Math.sqrt(px*px + py*py);
  px = (px / plen) * rx * spread * L;
  py = (py / plen) * ry * spread * L;

  const bx1 = tipX - ux * barbFrac + px;
  const by1 = tipY - uy * barbFrac + py;
  const bz1 = tipZ - uz * barbFrac;

  const bx2 = tipX - ux * barbFrac - px;
  const by2 = tipY - uy * barbFrac - py;
  const bz2 = tipZ - uz * barbFrac;

  return {
    x: [x0, tipX, bx1, null, tipX, bx2],
    y: [y0, tipY, by1, null, tipY, by2],
    z: [z0, tipZ, bz1, null, tipZ, bz2]
  };
}

function renderState(epochIdx, isGrad) {
  currentEpoch = Math.max(0, Math.min(data.length - 1, epochIdx));
  showGradient = isGrad;
  const d = data[currentEpoch];

  const pathX = w1_vals.slice(0, currentEpoch + 1);
  const pathY = w2_vals.slice(0, currentEpoch + 1);
  const pathZ = loss_vals.slice(0, currentEpoch + 1);

  let arrow = { x: [null], y: [null], z: [null] };
  if (showGradient && currentEpoch < data.length - 1) {
    const next = data[currentEpoch + 1];
    arrow = computeStickArrow(d.w1, d.w2, d.loss, next.w1, next.w2, next.loss);
  }

  Plotly.restyle('plot', { x: [pathX], y: [pathY], z: [pathZ] }, [1]);
  Plotly.restyle('plot', { x: [[d.w1]], y: [[d.w2]], z: [[d.loss]] }, [2]);
  Plotly.restyle('plot', { x: [arrow.x], y: [arrow.y], z: [arrow.z] }, [3]);
}

window.addEventListener('message', (e) => {
  if (e.data && typeof e.data.progress === 'number') {
    const p = Math.max(0, Math.min(1, e.data.progress));
    const totalPhases = (data.length - 1) * 2;
    const phaseIdx = Math.floor(p * totalPhases);
    const epoch = Math.floor(phaseIdx / 2);
    const isGrad = (phaseIdx % 2 === 1);
    renderState(epoch, isGrad);
  }
});

renderState(0, false);
</script>
</body>
</html>
"""

full_bg_html = bg_html.replace("DATA_PLACEHOLDER", json.dumps(steps))

with open("assets/gradient_descent_bg.html", "w") as f:
    f.write(full_bg_html)

print("Generated assets/gradient_descent_bg.html successfully.")
