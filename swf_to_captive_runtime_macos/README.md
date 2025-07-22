## Example Usage

```commandline
python3 swf_to_captive_runtime.py --air-sdk-bin-path $HOME/Downloads/AIRSDK_MacOS/bin  --source-swf-path SetBackground.swf --executable-name PinkbackgroundApplication --window-title "Pink Background App" --runtime-output-path ./PinkbackgroundBundle
```
## Example Output/Directory Structure
```
├── PinkbackgroundBundle.app
│   └── Contents
│       ├── Frameworks
│       │   └── Adobe AIR.framework
│       │       ├── Adobe AIR -> Versions/Current/Adobe AIR
│       │       ├── Resources -> Versions/Current/Resources
│       │       └── Versions
│       │           ├── 1.0
│       │           │   ├── Adobe AIR
│       │           │   ├── Resources
│       │           │   │   ├── Adobe Root Certificate.cer
│       │           │   │   ├── Info.plist
│       │           │   │   ├── Licenses
│       │           │   │   │   └── pcre2
│       │           │   │   │       └── COPYING
│       │           │   │   ├── Thawte Root Certificate.cer
│       │           │   │   ├── cs.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── de.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── en.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── es.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── fr.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── it.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── ja.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── ko.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── nl.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── pl.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── pt.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── ru.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── sv.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── tr.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   ├── zh_Hans.lproj
│       │           │   │   │   ├── AuthDialog.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   ├── ContentUIText.xml
│       │           │   │   │   ├── Localizable.strings
│       │           │   │   │   ├── MainMenu.nib
│       │           │   │   │   │   └── keyedobjects.nib
│       │           │   │   │   └── PlayerUILocalizable.strings
│       │           │   │   └── zh_Hant.lproj
│       │           │   │       ├── AuthDialog.nib
│       │           │   │       │   └── keyedobjects.nib
│       │           │   │       ├── ContentUIText.xml
│       │           │   │       ├── Localizable.strings
│       │           │   │       ├── MainMenu.nib
│       │           │   │       │   └── keyedobjects.nib
│       │           │   │       └── PlayerUILocalizable.strings
│       │           │   └── _CodeSignature
│       │           │       └── CodeResources
│       │           └── Current -> 1.0
│       ├── Info.plist
│       ├── MacOS
│       │   └── PinkbackgroundApplication
│       ├── PkgInfo
│       └── Resources
│           ├── META-INF
│           │   ├── AIR
│           │   │   ├── application.xml
│           │   │   └── hash
│           │   └── signatures.xml
│           ├── application.swf
│           └── mimetype
├── README.md
├── SetBackground.swf
├── airhelper.py
└── swf_to_captive_runtime.py
[air_helper.py](../actionscript_to_captive_runtime_01/air_helper.py)
```


### Bundling - Permission Requirements

When an application bundle has been made for the captive runtime along with a SWF, the special directory made must have execute permissions in order for the user to be able to click on and open it. By default the .app directory output by the adt utility will have execute permissions. It may be possible that as part of a broader bundling process of our own such as for the ambassador, that we do not preserve these permissions in the archive that we make and that it won't be able to be executed.

#### Findings 1 - chmod 660 (execute permissions MUST to be kept)
Setting the application bundle directory to be only readable and writable by the user and group while executable by no on resulted in clicking on the file resulting in an error of 'The application "captive_runtime" can't be opened' [\[1\]](https://ibb.co/d41Ky0qs) [\[2\]](https://ibb.co/DgKxGWbk)

#### Findings 2 - Filename does matter
The filename as used on windows to get a result like runtime_directory/RequiemWorld.exe determines the executable named used on macos in the same capacity. The application bundle is executed but inside of it the process that will be started is named the same. Example: If the executable name used is "RequiemWorld" then when executed, the process will show up in top as "RequiemWorld", while what the user interacts with to open it is the directory name. 

- The executable is located inside the bundle at Contents/MacOS/{filename} e.g. PinkbackgroundBundle.app/Contents/MacOS/PinkbackgroundApplication

#### Findings 3 - Bundled SWF location

The main SWF of the application for the captive runtime to use is located in the resources directory of the application bundle e.g. PinkbackgroundBundle.app/Contents/Resources/application.swf

- This file is of interest because we may wish to produce captive runtime bundles ahead of time for the sake of switching out the SWF file used inside, e.g. take one of our pre-bundled runtimes and switch the SWF file in use for mac from windows or linux.

#### Findings 4 - Bundled Application Descriptor
The application descriptor file is located at Contents/Resources/META-INF/application.xml, and can be modified without rebundling anything. The width and height were able to be changed to 1920x1080, leaving the application in a working state. 

#### Findings 5 - Name in top left corner
- The name in the top left corner for the application on MacOS seemed to usually show as the executable name (PinkbackgroundApplication) but suddenly showed "AIR Helper". The application will show the name of the application from the descriptor when it is first started but then on certain inputs such as hitting ctrl, will change to the name of the executable.
    - The window title and filename seemed to matter more than the name on windows. On MacOS the name section **does** matter. 