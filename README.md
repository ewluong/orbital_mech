# Orbital Mechanics Holographic Simulator

Welcome to the **Orbital Mechanics Simulator**!

## Overview

This simulator leverages **Three.js** for rendering a dynamic, interactive 3D scene, **Chart.js** for real-time data visualization, and a custom physics engine to simulate the gravitational interactions of celestial bodies. You'll see planets, moons, and even custom orbits come alive in a holographic style.

> Personally, I think nothing beats seeing the cosmos dance right on your browser. It’s a fun mix of art and science!

## Features

- **3D Visualization:** Explore a stunning 3D simulation of our solar system with realistic orbital mechanics.
- **Interactive HUD:** Keep track of simulation time, energy, momentum, and other key metrics.
- **Custom Orbits:** Easily add your own celestial bodies and define custom orbits.
- **Real-Time Charts:** Watch data evolve in real time with integrated Chart.js graphs.
- **Multiple Integrators:** Toggle between RK4 and Leapfrog integration methods for different simulation experiences.
- **Responsive Controls:** Adjust time scale, reset the simulation, and export simulation data with a single click.

## Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, or Edge recommended)
- A local server environment (optional, but recommended for full functionality)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/3d-holographic-solar-system-simulator.git
   cd 3d-holographic-solar-system-simulator
   ```

2. **Open the Project:**

   Simply open the `index.html` file in your web browser. For the best experience, consider running a local server:

   ```bash
   # Using Python 3.x
   python -m http.server 8000
   ```

   Then navigate to `http://localhost:8000` in your browser.

### Usage

- **Navigation:** Click and drag to rotate your view. Use the mouse wheel to zoom in/out.
- **Controls:**
  - **Speed Up/Slow Down:** Adjust the simulation time scale.
  - **Reset:** Restart the simulation.
  - **Data HUD:** Toggle the real-time data display.
  - **Toggle Integrator:** Switch between RK4 and Leapfrog methods.
  - **Export Data:** Download simulation data as a CSV file.
- **Custom Orbits:** Use the sliders to set parameters like mass, semi-major axis, eccentricity, etc., and add your own orbit to the simulation.

## Technical Details

- **Three.js:** Used for rendering the 3D scene and creating a holographic effect.
- **Chart.js:** Provides real-time graphs displaying energy, momentum, and other physical properties.
- **Custom Physics Engine:** Implements gravitational interactions with both RK4 and Leapfrog integrators for accuracy and performance.
