# SWF Sample Acquisition

For security purposes on the project we require access to SWFs that contain in individuality each thing that we want our security solution to scan and block. SWF files come in three variations that each need to be identified, decompressed (if applicable) and blocked, failure to detect and scan one of them (for example, only knowing about commonly compiled with ZLIB compression, and no compression, and not lzma compression) would result in easy evasion of the security solution and [severe damage](https://help.adobe.com/en_US/as3/dev/WS5b3ccc516d4fbf351e63e3d118666ade46-7e5a.html) on the table again due to the loadBytes/main application issue in the game client.

## Acquiring Samples

We are acquiring samples by writing the code to contain what we want to detect, compiling it ourselves (without compression) and using tools to apply compression to the main part. To acquire a sample of a SWF file that will use ``flash.filesystem.File``, we can import it and assign a variable to an instance of it, then prepare the three variations of it. Compiling a SWF can be done with mxmlc from the AIR sdk, and since harmon took over, a utility has been provided officially with the SDK which can notably turn an non-compressed SWF into an LZMA variant or ZLIB variant.

## Variant Maker

A script has been made (variant_maker.py) to automate the process of taking an actionscript file, compiling it, and producing the three varieties. The easiest way to use the script is to download the harmon air sdk for windows, ensure java is installed, extract it, and add the bin directory to the system path, and then the script can automatically find it and use it as needed. Assure that the version of harmon AIR used has ``swfcompress.bat`` in the bin directory.

Example Usage
```commandline
python .\variant_maker.py .\flash-filesystem-file-usage/Main.as FlashFileSystemFile.swf
```
Example Result
```
made no compression variant of swf for .\flash-filesystem-file-usage\Main.as at C:\Users\<redacted>\Documents\swf_sample_creation\flash-filesystem-file-fws.swf
made lzma compression variant of swf for .\flash-filesystem-file-usage\Main.as at C:\Users\<redacted>>\Documents\swf_sample_creation\flash-filesystem-file-zws.swf
made zlib compression variant of swf for .\flash-filesystem-file-usage\Main.as at C:\Users\<redacted>\Documents\swf_sample_creation\flash-filesystem-file-cws.swf
```


The first argument is the path to the script to compile, the second is the base name of the SWF being output, optionally an --output-directory can be provided to tell the script where to put the output files. When .swf is in the base name, the signature (cws, fws, fws) will be tacked on before the extension like BaseName-fws.swf.

## Additional Notes
- The explicit choice has been made to put the scripts that we are compiling into their own directories with descriptive names. We want to make sure that when we scan a SWF for something like flash.net.Filesystem, we don't open room for a situation where the symbol of our main class could be what we are detecting and not what we actually want to block.
  - To ensure that when we scan a SWF file we are actually detecting and blocking what we want, we just keep it plain and name it Main.
- An extra emphasis was placed into automating this and putting together some of the actionscript used to create the samples required for the firewalling portion of the ambassador, for the sake of documentation and reproducibility. Any actionscript file should be able to be turned into all three required variants with limited room for human error. Should more samples be needed in the future, the provided script can be used to get them swiftly.
- Adobe/Harmon AIR is actively maintained and extended. It may be possible that a new compression variety of SWF file may be introduced leaving clients with newer versions vulnerable. Care should be placed in the distant future in updating AIR versions on applications that require protection (i.e., the game client). 