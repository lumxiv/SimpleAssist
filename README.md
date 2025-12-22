# SBlenderAssist

An add-on to import/export FFXIV animations using Blender. Based on [BlenderAssist](https://github.com/0ceal0t/BlenderAssist)

## Requirements

- [VC++2012 32-bit Redist](https://www.microsoft.com/en-us/download/details.aspx?id=30679#) (`VSU_4\vcredist_x86.exe`)
- [Blender 4.5](https://www.blender.org/)
- [VFXEditor](https://github.com/0ceal0t/Dalamud-VFXEditor)

## Installation
Download the addon from the [releases](https://github.com/lumxiv/SBlenderAssist/releases).  
Go to `Edit > Preferences > Add-ons > Install From Disk...` and select the entire `.zip` file. Make sure to enable the add-on as well.

> Note on updating: you may need to uninstall the add-on, restart Blender, and then re-install it

<img width="661" height="547" alt="blender_i2ui8NeGyk" src="https://github.com/user-attachments/assets/11889a9f-b635-4d70-9ce3-c314a39dece7" />

## Quick Start
### Import
<img width="257" height="210" alt="blender_ZMMKdWbViU" src="https://github.com/user-attachments/assets/637ce1b5-1ff5-4f33-9f01-5e4eee66d249" />

### Export
<img width="253" height="258" alt="blender_Qe7vDGpFg9" src="https://github.com/user-attachments/assets/7481706b-10f9-486d-95a1-2d783ea6fcee" />

## Editing FFXIV

See [this document](https://docs.google.com/document/d/136lDxkzdA7ZUULS_fGWDrd_1NsBvTSdtDCbSfNRZ-DE/edit?usp=sharing)

## Notes on Building

This is taken verbatim from [AnimAssist](https://github.com/lmcintyre/AnimAssist#building):

> Building animassist.exe requires the Havok 2014 SDK and an env var of HAVOK_SDK_ROOT set to the directory, as well as the Visual C++ Platform Toolset v110. This is included in any install of VS2012, including the Community edition. You can find the Havok SDK to compile with in the description of [this video](https://www.youtube.com/watch?v=U88C9K-mSHs). Please note that is NOT a download I control, just a random one from online.

Make sure to set your `HAVOK_SDK_ROOT` like this:

![image](https://user-images.githubusercontent.com/18051158/162323294-f6eacc56-7efc-4cf4-9247-ac3888ee865a.png)
