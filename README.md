<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

#### Windows install part A (checked on Windows 10 and 11)

1. Install Python 3.11.7 https://www.python.org/downloads/windows/ . Download correct installer package for your computer. Run .exe program. When you run the installer **YOU MUST CHECK** *"Install launcher for all users"* AND **"Add Python 3.11 to PATH"**. Then run *"Install Now"*

2. Install Pip (Python's package management system):
   ```sh
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   python get-pip.py
   ```
   Edit the environment variables and add the Pip´s PATH, copying it from the command prompt.

3. Install Fluidsynth installer (will need to open PowerShell as administrator)
   1. Go to the FluidSynth releases page https://github.com/FluidSynth/fluidsynth/releases
   2. Download the latest 64-bit release for Windows (e.g. fluidsynth-2.1.0-win64.zip). Extract this zip file into some directory, e.g. c:\Users\me\install\fluidsynth.
   3. Move the 'bin' folder from 'fluidsynth' into 'install' folder.
   4. Add the C:\Users\me\install\bin subdirectory to your PATH. To do this, click in the search box on the task bar, run the command 'Edit the system environment variables', click 'Environment Variables…', select Path in the 'User variables' section, click 'Edit…', click New, then enter the path of the bin subdirectory, e.g. c:\Users\me\install\bin . NB It may have automatically done this

4. Install Git (64-bit Git for Windows Setup) accepting all the default options: https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe

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
4. Install the dependencies
   ```sh
   pip install -r requirements.txt
   ```


### Running the app

1. Enter the main APP folder
   ```sh
   cd machainst
   ```
2. Execute the code
   ```sh
   python main.py
   ```
