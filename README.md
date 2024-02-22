<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

#### Windows install part A (checked on Windows 10 and 11)

1. Install Python 3.11.7 https://www.python.org/downloads/windows/ . Download correct installer package for your computer. Run .exe program. When you run the installer **YOU MUST CHECK** *"Install launcher for all users"* AND **"Add Python 3.11 to PATH"**. Then run *"Install Now"*

2. Install Fluidsynth installer (will need to open PowerShell as administrator)
   1. Go to the FluidSynth releases page https://github.com/FluidSynth/fluidsynth/releases
   2. Download the latest 64-bit release for Windows (e.g. fluidsynth-2.1.0-win64.zip). Extract this zip file into some directory, e.g. c:\Users\me\install\fluidsynth.
   3. Move the 'bin' folder from 'fluidsynth' into 'install' folder.
   4. Add the C:\Users\me\install\bin subdirectory to your PATH. To do this, click in the search box on the task bar, run the command 'Edit the system environment variables', click 'Environment Variables…', select Path in the 'User variables' section, click 'Edit…', click New, then enter the path of the bin subdirectory, e.g. c:\Users\me\install\bin . NB It may have automatically donw this

3. Install Poetry with the official installer (will need to open PowerShell as administrator). Follow the instructions at: https://python-poetry.org/docs/#installing-with-the-official-installer

#### MacOS install part A

1. Install HomeBrew. Follow instructions at: https://brew.sh/
2. Install Fluidsynth in HomeBrew
   ```sh
   brew install fluidsynth
   ```
   
#### Install part B (Windows 10 & 11, Linux and MacOS)

1. Open a Terminal window (Mac & Linux) or a Command Prompt (Windows: in the toolbar search type 'command prompt', and open as user).

2. Clone the repo
   ```sh
   git clone https://github.com/DigiScore/machAInst.git
   ```
3. Navigate to the folder
   ```sh
   cd machAInst
   ```
4. Activate the Poetry environment
   ```sh
   poetry shell
   ```
5. Install the dependencies
   ```sh
   poetry install
   ```


### Running the app

1. Enter the main APP folder
   ```sh
   cd machainst
   ```
2. Execute the code
   ```sh
   poetry run python main.py
   ```
