# NeuroTechWorkshop

Educational neurotechnology workshop featuring EEG simulations, Fourier signal decomposition, neuron anatomy animations, brain-wave state visualizations, and Fourier epicycle drawing from images. Built for neuroscience and signal-processing learning using Manim and Python.

---

## Repository Structure

```
NeuroTechWorkshop/
├── epicycles.py          # Fourier epicycle drawing pipeline from any image
├── brainwaves.py         # Manim animation of EEG brain-wave states (Delta to Gamma)
├── fourierwave.py        # Manim Fourier decomposition of a complex EEG signal
├── neuron.py             # Manim animation of a neuron and signal propagation
├── test.py               # Minimal Manim smoke test
├── requirements.txt      # Python dependencies
└── README.md
```

---

## Prerequisites

- Python 3.9 or higher
- pip
- For Manim scenes: a working LaTeX distribution (for text rendering) and FFmpeg (for video export)

### Installing system dependencies

**Ubuntu / Debian**

```bash
sudo apt update
sudo apt install ffmpeg texlive texlive-latex-extra
```

**macOS (Homebrew)**

```bash
brew install ffmpeg
brew install --cask mactex
```

**Windows**

Download and install FFmpeg from https://ffmpeg.org/download.html and add it to your PATH. Install MiKTeX from https://miktex.org/download for LaTeX support.

---

## Setup

Clone the repository and install Python dependencies.

```bash
git clone https://github.com/<your-username>/NeuroTechWorkshop.git
cd NeuroTechWorkshop
```

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If you only want to run `epicycles.py` without Manim, the minimal install is:

```bash
pip install numpy matplotlib opencv-python
```

---

## Running the Manim Scenes

Manim renders scenes as video files. The general command is:

```bash
manim -pql <filename.py> <ClassName>
```

Flags:
- `-p` — preview the video after rendering
- `-q l` — low quality (480p), fast render; use `m` for 720p or `h` for 1080p
- `-q h` — high quality (1080p), slower render

### Verify your Manim installation

```bash
manim -pql test.py Hello
```

This renders a simple "Hello Manim" text animation. If it plays without errors, your setup is working.

### Brain-wave state visualization

Animates the transition from Delta waves (deep sleep) through Theta, Alpha, Beta, and Gamma states, with a pulsing brain diagram and live waveform.

```bash
manim -pql brainwaves.py BrainWaveVisualization
```

For a higher quality render:

```bash
manim -pqh brainwaves.py BrainWaveVisualization
```

### Fourier decomposition of an EEG signal

Shows a complex EEG signal being decomposed into its component brain-wave frequencies (beta, alpha, theta, delta) with an animated frequency spectrum.

```bash
manim -pql fourierwave.py FourierDecomposition
```

### Neuron anatomy and signal propagation

Builds a full neuron from soma to axon terminals and animates signal particles travelling from dendrites through to the axon.

```bash
manim -pql neuron.py NeuronScene
```

---

## Running the Epicycles Script

`epicycles.py` is a standalone script and does not require Manim. It takes any image, extracts its dominant contour using OpenCV edge detection, computes the Discrete Fourier Transform, and animates the resulting epicycle chain drawing the shape.

### Basic usage

```bash
python epicycles.py --image path/to/image.png
```

### Options

| Flag | Default | Description |
|---|---|---|
| `--image` | required | Path to the input image (JPEG, PNG, etc.) |
| `--n_terms` | 100 | Number of epicycles to use in reconstruction |
| `--n_points` | 1024 | Resampling resolution of the extracted contour |
| `--n_frames` | 400 | Animation frames per full revolution |
| `--canny_lo` | 30 | Lower threshold for Canny edge detection |
| `--canny_hi` | 100 | Upper threshold for Canny edge detection |
| `--strategy` | longest | Contour selection: `longest` or `largest` |
| `--multi` | off | Animate all contours as separate colour-coded strokes |
| `--diagnostics` | off | Show edge-detection diagnostic plots before animating |
| `--save` | None | Save animation to a `.gif` or `.mp4` file |

### Examples

Draw a silhouette with 150 epicycles and save as GIF:

```bash
python epicycles.py --image cat.jpg --n_terms 150 --save output.gif
```

Animate every detected contour as a separate stroke:

```bash
python epicycles.py --image logo.png --multi
```

Inspect what the edge detector is picking up before running the full animation:

```bash
python epicycles.py --image photo.jpg --diagnostics
```

Save as MP4 (requires FFmpeg):

```bash
python epicycles.py --image shape.png --n_frames 600 --save output.mp4
```

---

## Output Files

Manim writes rendered videos to a `media/` folder in the project directory, organized by quality:

```
media/
└── videos/
    └── <filename>/
        └── <quality>/
            └── <ClassName>.mp4
```

For example, a low-quality render of `BrainWaveVisualization` will appear at:

```
media/videos/brainwaves/480p15/BrainWaveVisualization.mp4
```

---

## Troubleshooting

**`cairo` or `pango` errors on Linux**

```bash
sudo apt install libcairo2-dev libpango1.0-dev
```

**`manim` command not found after install**

Ensure your virtual environment is activated, or try:

```bash
python -m manim -pql test.py Hello
```

**OpenCV import error in epicycles.py**

```bash
pip install opencv-python
```

**FFmpeg not found when saving `.mp4`**

Install FFmpeg and confirm it is on your PATH:

```bash
ffmpeg -version
```

**Blank or empty animation from epicycles.py**

Try adjusting the Canny thresholds. Lower values pick up more edges; higher values are more selective:

```bash
python epicycles.py --image photo.jpg --canny_lo 10 --canny_hi 60 --diagnostics
```

---

## License

This project is for educational use.
Authors: Parth Pancholi, Saurav Kumar
Institution: VIT Bhopal