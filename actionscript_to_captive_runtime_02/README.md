
## Example Usage

The following command will take a path to the root actionscript file of a project (or just a standalone actionscript file) to compile into a SWF, and then will create an application descriptor for the SWF and bundle it with the captive runtime. A throw away signing certificate will be generated and used to sign it. The primary arguments are the path to the actionscript to compile, and the directory that the captive runtime/application SWF should be placed in. 

```commandline
py .\as3_to_captive_runtime.py .\SetBackground\SetBackground.as .\PinkBackgroundApplication --runtime-executable-name PinkBackgroudApp
```
## Example Success

When an actionscript file is successfully compiled in the above command, the directory "PinkBackgroundApplication" will contain ``PinkBackgroundApp.exe`` and ``application.swf``. The actionscript at this point has been compiled, and the application can be ran from what is in this directory alone, with it ready for distribution. Additional options are available such as setting the window title and application version number.
```
actionscript_to_captive_runtime/PinkBackgroundApplication/
├── Adobe AIR
│   └── Versions
│       └── 1.0
│           ├── Adobe AIR.dll
│           ├── Adobe AIR.dll:Zone.Identifier:$DATA
│           └── Resources
│               ├── Adobe AIR.vch
│               ├── Adobe AIR.vch:Zone.Identifier:$DATA
│               ├── adobecp.vch
│               ├── adobecp.vch:Zone.Identifier:$DATA
│               ├── CaptiveAppEntry.exe
│               ├── CaptiveAppEntry.exe:Zone.Identifier:$DATA
│               ├── CaptiveCmdEntry.exe
│               ├── CaptiveCmdEntry.exe:Zone.Identifier:$DATA
│               └── Licenses
│                   ├── cairo
│                   │   ├── COPYING
│                   │   ├── COPYING-LGPL-2.1
│                   │   ├── COPYING-LGPL-2.1:Zone.Identifier:$DATA
│                   │   ├── COPYING-MPL-1.1
│                   │   ├── COPYING-MPL-1.1:Zone.Identifier:$DATA
│                   │   └── COPYING:Zone.Identifier:$DATA
│                   ├── pcre2
│                   │   ├── COPYING
│                   │   └── COPYING:Zone.Identifier:$DATA
│                   └── pixman
│                       ├── COPYING
│                       └── COPYING:Zone.Identifier:$DATA
├── application.swf
├── META-INF
│   ├── AIR
│   │   ├── application.xml
│   │   └── hash
│   └── signatures.xml
├── mimetype
└── PinkBackgroudApp.exe

```