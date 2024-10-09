<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

#### Windows install part A (checked on Windows 10 and 11)

1. Install `scoop`, (a command-line installer for Windows). 
Open a `PowerShell` terminal as administrator and execute the following commands (one at a time):

   A) Install Scoop
      ```shell
      Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
      ```
   
      OPTIONAL - Type 'Y' to continue

      ```shell
      Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
      ```   

   B) Install Git 
      ```shell
      scoop install git
      ```

   C) Install poetry
      ```shell
      scoop install main/poetry
      ```

   D) Uninstall incorrect version of python
      ```shell
      scoop uninstall python
      ```

   E) Install correct python version
      ```shell
      scoop install python@3.11.6
      ```

   F) Install Fluidsynth
   
      ```shell
      scoop bucket add extras
      ```
      
      ```shell
      scoop install extras/fluidsynth
      ```
   G) Add Fluidsynth to PATH   

      Add the `C:\Users\me\scoop\apps\fluidsynth\current\bin` subdirectory to your PATH (change 'me' to your username) . 
To do this, click in the search box on the task bar, run the command 'Edit the system environment variables', click 'Environment Variables…', select Path in the 'User variables' section, click 'Edit…', click New, then enter the path of the bin subdirectory, e.g. `C:\Users\me\scoop\apps\fluidsynth\current\bin`  (change 'me' to your username) . NB It may have automatically done this.)

[//]: # (5. Install Fluidsynth installer)

[//]: # (   1. Go to the FluidSynth releases page https://github.com/FluidSynth/fluidsynth/releases)

[//]: # (   2. Download the latest 64-bit release for Windows &#40;e.g. fluidsynth-2.1.0-win64.zip&#41;. )

[//]: # (   3. Extract this zip file into some directory, e.g. c:\Users\me\install\fluidsynth. &#40;NB replace 'me' with your username&#41;)

[//]: # (   4. Move the 'bin' folder from 'fluidsynth' into 'install' folder &#40;drag and drop from the folder&#41;. )

[//]: # (   5. Add the `C:\Users\me\scoop\apps\fluidsynth\current\bin` subdirectory to your PATH. To do this, click in the search box on the task bar, run the command 'Edit the system environment variables', click 'Environment Variables…', select Path in the 'User variables' section, click 'Edit…', click New, then enter the path of the bin subdirectory, e.g. `C:\Users\me\scoop\apps\fluidsynth\current\bin` . NB It may have automatically done this.)

[//]: # ()


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
   
6. Close the Terminal window 

–––––––––––––––––––––

### Running the app (ALL PLATFORMS)

1. Open a new Terminal window (Mac & Linux) or a Command Prompt (Windows: in the toolbar search type 'command prompt', and open as user).


2. Navigate to the folder
   ```sh
   cd joyinst
   ```
   
3. Activate poetry
   ```sh
   poetry shell
   ```
     
4. Enter the main APP folder
   ```sh
   cd joyinst
   ```

5. Execute the code
   ```sh
   poetry run python main.py
   ```
