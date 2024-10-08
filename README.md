<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

#### Windows install part A (checked on Windows 10 and 11)

1. Install `scoop`, (a command-line installer for Windows). Open a `PowerShell` terminal and execute the following commands (one at a time):
   ```shell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   ```shell
   Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
   ```   

2. Install Git (64-bit Git for Windows Setup) accepting all the default options: https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe

3. Open a regular `Command Prompt (cmd)` and execute  (one at a time):
   ```shell
   scoop bucket add main
   ```
   
   ```shell
   scoop install main/poetry
   ```
   
   Do not close the `Command Prompt` window. We will use it again.

   
4. Install `Fluidsynth`, using the same `Command Prompt` from step 2:
   ```shell
   scoop bucket add extras
   ```
   
   ```shell
   scoop install extras/fluidsynth
   ```
   
5. Install Fluidsynth installer
   1. Go to the FluidSynth releases page https://github.com/FluidSynth/fluidsynth/releases
   2. Download the latest 64-bit release for Windows (e.g. fluidsynth-2.1.0-win64.zip). 
   3. Extract this zip file into some directory, e.g. c:\Users\me\install\fluidsynth. 
   4. Move the 'bin' folder from 'fluidsynth' into 'install' folder. 
   5. Add the `C:\Users\me\scoop\apps\fluidsynth\current\bin` subdirectory to your PATH. To do this, click in the search box on the task bar, run the command 'Edit the system environment variables', click 'Environment Variables…', select Path in the 'User variables' section, click 'Edit…', click New, then enter the path of the bin subdirectory, e.g. `C:\Users\me\scoop\apps\fluidsynth\current\bin` . NB It may have automatically done this.



–––––––––––––––––––––


#### MacOS install part A

1. Install HomeBrew. Follow instructions at: https://brew.sh/
2. Install Fluidsynth in HomeBrew
   ```sh
   brew install fluidsynth
   ```
 
–––––––––––––––––––––

  
#### Install part B (ALL PLATFORMS: Windows 10 & 11, Linux and MacOS)

1. Open a Terminal window (Mac & Linux) or a Command Prompt (Windows: in the toolbar search type 'command prompt', and open as user).

2. Clone the repo
   ```sh
   git clone https://github.com/DigiScore/joyinst.git
   ```
   
3. Navigate to the folder
   ```sh
   cd joyinst
   ```
   
4. Install the dependencies (one at a time)
   ```sh
   poetry shell
   ```
   
   ```shell
   poetry install
   ```

–––––––––––––––––––––

### Running the app (ALL PLATFORMS)

1. Navigate to the folder
   ```sh
   cd joyinst
   ```
   
2. Activate poetry
   ```sh
   poetry shell
   ```
     
3.  Enter the main APP folder
   ```sh
   cd joyinst
   ```

4. Execute the code
   ```sh
   poetry run python main.py
   ```
