# Orbital Mechanics Simulator

Welcome to the **Orbital Mechanics Simulator**! This project is a visually engaging and feature-rich simulation of celestial mechanics with a futuristic, cyberpunk aesthetic. The simulator models gravitational interactions between bodies, supports multiple numerical integration methods, and offers a dynamic, interactive GUI.

---

## Features

- **Gravitational Simulation:**  
  Simulate the motion of celestial bodies under mutual gravitational forces using both Euler and Runge-Kutta (RK4) integration methods.

- **Interactive Body Creation:**  
  Create new planets on-the-fly by using Shift + Click & Drag to define their initial position and velocity.

- **Collision Merging:**  
  When bodies collide, they merge into a single body with conserved momentum and mass.

- **Orbit Trails:**  
  Visualize the path of each celestial body with fading trails that provide a motion blur effect.

- **Dynamic Starfield Background:**  
  Explore a procedurally generated cosmic backdrop that moves as you pan and zoom.

- **Camera Controls:**  
  Pan the simulation view with right-click dragging and zoom in/out using the mouse wheel.

- **Minimap:**  
  A small minimap in the top-right corner displays a scaled view of the simulation’s boundaries and the positions of all bodies.

- **Body Selection & Trajectory Prediction:**  
  Select a body by clicking on it (without holding Shift) to view its short-term predicted trajectory, visualized as a dashed neon-green line.

- **Real-time Energy Statistics:**  
  Monitor the system’s kinetic and potential energy, displayed on the screen for insight into energy conservation.

- **Screenshot Capability:**  
  Capture the current view of your simulation with a single button press.

- **Streamlined GUI:**  
  A set of intuitive buttons and sliders (positioned at the bottom left and top areas) lets you adjust simulation speed, gravitational constant, planet size, and more.

---

## Installation

### Requirements

- **Python 3.10+**  
- **Pygame** (tested with Pygame 2.6.1)  
  You can install Pygame via pip:

  ```bash
  pip install pygame
  ```

### Download

Clone this repository or download the source files:
- `main.py`
- `entities.py`
- `physics.py`
- `gui.py`
- `utils.py`

---

## Usage

To start the simulator, navigate to the project directory and run:

```bash
python main.py
```

### Controls

- **Simulation Controls:**  
  - **Pause/Resume:** Click the "Pause/Resume" button.
  - **Reset Simulation:** Click the "Reset" button.
  - **Integration Method:** Toggle between Euler and RK4 using the "Integration" button.
  - **Debug Mode:** Toggle debug vectors with the "Debug" button.
  - **Reset Camera:** Click "Reset Camera" to re-center and reset the zoom.
  - **Screenshot:** Capture the current view by clicking "Screenshot".

- **Interactive Creation:**  
  - **Create Planet:** Hold **Shift** and drag the left mouse button to create a new body with initial velocity determined by the drag vector.

- **Camera Controls:**  
  - **Pan:** Right-click and drag to pan the view.
  - **Zoom:** Use the mouse wheel to zoom in or out.

- **Prediction & Selection:**  
  - **Select Body:** Click (without holding Shift) on a body to select it.
  - **Trajectory Prediction:** Toggle prediction using the "Prediction" button to see a short-term trajectory of the selected body.
  - **Clear Selection:** Click the "Clear Selection" button to deselect any selected body.

- **GUI Sliders (Bottom Left):**  
  - **Sim Speed:** Adjusts the simulation speed.
  - **Planet Size:** Controls the size (and mass) of new bodies.
  - **G Constant:** Adjusts the gravitational constant.

- **Legend (Bottom Right):**  
  Briefly displays key camera controls: Shift+Drag (create), right-drag (pan), and mouse wheel (zoom).

- **Minimap (Top Right):**  
  Displays a scaled overview of the simulation with the positions of all bodies.

---

## Project Structure

- **main.py:**  
  The entry point of the application. Handles event processing, simulation loop, camera controls, drawing the starfield, minimap, and managing GUI interactions.

- **entities.py:**  
  Contains the `CelestialBody` class, representing celestial objects with properties like mass, velocity, position, and methods for updating state and drawing.

- **physics.py:**  
  Implements gravitational force calculations and numerical integration methods (Euler and RK4) for updating the simulation.

- **gui.py:**  
  Defines GUI components including buttons and sliders, along with helper functions for drawing UI elements.

- **utils.py:**  
  Provides utility functions for vector operations and other helper methods.

---



