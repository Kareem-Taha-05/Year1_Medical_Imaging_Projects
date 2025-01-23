# 3D Brain Puzzle Game

# Description
The 3D Brain Puzzle Game challenges players to reconstruct a scattered brain by moving and rotating individual parts. Players must align and assemble the pieces into a complete brain structure. This interactive and engaging game combines problem-solving and spatial awareness, offering an immersive 3D puzzle-solving experience.

Built using Unity, the game leverages 3D physics, intuitive controls, and visually appealing assets to create an educational and entertaining experience.

# Features

- **Engaging Gameplay**:
  - Players interact with individual brain parts to rotate, move, and align them correctly.
  - Dynamic feedback guides players as they progress toward assembling the brain.
- **Intuitive Controls**:
  - Click and drag to move objects in 3D space.
  - Rotate parts using on-screen gestures or dedicated rotation buttons.
  - Snap-to-position mechanics for precise alignment.
- **Immersive 3D Environment**:
  - High-quality brain models with realistic textures.
  - Rotatable camera for a full 360° view of the puzzle.
- **Progress Tracking**:
  - Sound cues indicate correctly placed parts.
  - A Timer that tracks the player's progress and tells the players how long they took to complete the puzzle.

# File Content
## Scenes
  - Main Menu: The starting interface where players can choose levels and adjust settings.
  - Game Scene: The primary gameplay environment for assembling the brain.
  - Completion Screen: Displays after the puzzle is completed, showing the player's score and time.
## Scripts
  - GameController:
    - Manages game state, player progress, and completion logic.
  - PieceController:
    - Handles movement and rotation of individual brain parts.
    - Implements snapping logic for precise placement.
  - CameraController:
    - Allows players to rotate and zoom the camera for better viewing angles.
  - UIController:
    - Manages user interface elements such as progress bars, buttons, and hints.
## Assets
  - 3D Models: Realistic brain parts divided into multiple pieces.
  - Textures: High-resolution materials for brain parts and environment assets.
## Audio:
  - Sound effects for interactions and completion feedback.

# Usage
  - Install Unity: Ensure you have Unity 2021.3 LTS or later installed.

  - Clone the Repository:
  - Clone the project files into your local system:
    ``` 
  git clone https://github.com/yourusername/3d-brain-puzzle-game.git
  cd 3d-brain-puzzle-game
    ``` 
  - Open the Project:
    - Open the project folder in Unity Hub and load the scene.

  - Play the Game:
    - Start the game by pressing the start new game button in the Main Menu.
    - Use the mouse and keyboard controls to move and rotate the brain parts.
  - Align and assemble all parts to complete the brain.

  - Build the Game:
    - Export the game for your target platform (Windows, macOS, or WebGL):
    - Open File > Build Settings.
    - Select the platform.
    - Click Build.

# Requirements
Unity 2021.3 LTS or later.
A system with a dedicated graphics card for optimal performance.

# LICENSE
This project is licensed under the MIT License.
