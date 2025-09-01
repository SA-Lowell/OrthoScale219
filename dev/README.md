# Dev Folder

This folder contains development tools for OrthoScale219.

## stubs/

Type hint files (.pyi) for strict typing in IDEs like VS Code or PyCharm. Includes stubs for:
- bpy/: Blender Python API (e.g., props.pyi, utils.pyi, types/).
- mathutils/: Blender math utilities.
- pytest/: Only used for the py files inside of /tests/

I created these to solve strict typing issues that were still occurring in the IDE even with `blender-stubs` and `fake-bpy-module` installed. In fact, make sure to install those alongside these type stubs.

To use: Add `stubs/` to your IDE's stub path for better autocompletion and type checking.

`blender-stubs`
```
pip install blender-stubs
```

`fake-bpy-module`
```
pip install fake-bpy-module
```

## Running Local Tests

While running through these steps, you can mostly ignore any of the "Notes" sections. Generally they are just provided for additional context and information that you most likely won't need, but in some cases you might.

Python version 3.13.7 is used for this, but it's probably a good idea to ensure you are using whatever the latest version of Python is at the time you are working through these instructions. However, it's always possible newer versions could have conflicts with the instructions provided here. The instructions for installing Python will also differ based on your operating system.

An additional note: This entire process utilizes pip for managing package installation; other methods are not covered. This guide would just bloat too much if I went beyond pip.

### 1. Install Python

<div style="margin-left: 2em;">
 <details>
  <summary>
   <h4 style="display: inline-block">Linux</h4>
  </summary>
  <div style="margin-left: 1em;">

For linux, you would use the following commands in terminal (Pick one of the 3 based on your current Linux OS)

   <details>
    <summary>
     <h4 style="display: inline-block">Ubuntu/Debian</h4>
   </summary>
   <div style="margin-left: 1em;">

```bash
sudo apt install python3
```

<details>
 <summary>
  <h4 style="display: inline-block">Notes</h4>
 </summary>

These are the general install directories.

- **Executables**:
    - `/bin/<pythonversion>`

- **Libraries**:

    - `/usr/lib/<pythonversion>/`

- **core modules**:
    - `/usr/lib/<pythonversion>/lib-dynload/`

- **Site-packages (for third-party modules)**:

    Will be one of the following

    - `/home/<username>/.local/lib/<pythonversion>/site-packages/`
    - `/usr/local/lib/<pythonversion>/dist-packages/`

</details>
   </div>
  </details>
  <details>
   <summary>
    <h4 style="display: inline-block">Fedora</h4>
   </summary>
   <div style="margin-left: 1em;">

```bash
sudo dnf install python3
```

<details>
 <summary>
  <h4 style="display: inline-block">Notes</h4>
 </summary>

These are the general install directories.

- **Executables**:
    - `/usr/bin/<pythonversion>`

- **Libraries**:
    - `/usr/lib64/<pythonversion>/`

- **core modules**:
    - `/usr/lib64/<pythonversion>/lib-dynload/`

- **Site-packages (for third-party modules)**:
    - `/usr/lib64/<pythonversion>/site-packages/`

</details>
   </div>
  </details>
  <details>
   <summary>
    <h4 style="display: inline-block">Arch</h4>
   </summary>
   <div style="margin-left: 1em;">

```bash
sudo pacman -S python
```

<details>
 <summary>
  <h4 style="display: inline-block">Notes</h4>
 </summary>

These are the general install directories.

- **Executables**:
    - `/usr/bin/<pythonversion>`

- **Libraries**:
    - `/usr/lib/<pythonversion>/`

- **core modules**:
    - `/usr/lib/<pythonversion>/lib-dynload/`

- **Site-packages (for third-party modules)**:
    - `/usr/lib/<pythonversion>/site-packages/`

</details>
   </div>
  </details>
 </div>
</details>
<details>
 <summary>
  <h4 style="display: inline-block">Windows</h4>
 </summary>

Use either of the following two links to download Python for Windows.

If you're browsing this page via a Windows session it will automatically give you a download link for Windows.

- https://www.python.org/downloads/

Alternatively, use this link instead and click on any of the "Windows installer" links to download the version you want.

- https://www.python.org/downloads/windows/

 <div style="margin-left: 1em;">
  <details>
   <summary>
    <h4 style="display: inline-block">Notes</h4>
   </summary>

- **Install directories:**

    If you only install Python for the current user

    - `<driveletter>:\Users\<username>\AppData\Local\Programs\Python\<pythonversion>\`

    If you install Python system wide (For all users)

    64 bit

    - `<driveletter>:\Program Files\<pythonversion>\`

    32 bit

    - `<driveletter>:\Program Files (x86)\<pythonversion>\`

- **Executables:**
    - `<driveletter>:\Users\<username>\AppData\Local\Programs\Python\<pythonversion>\`

- **Libraries:**
    - `<driveletter>:\Users\<username>\AppData\Local\Programs\Python\<pythonversion>\Lib\`

- **Core modules/DLLs:**
    - `<driveletter>:\Users\<username>\AppData\Local\Programs\Python\<pythonversion>\`
    - `<driveletter>:\Users\<username>\AppData\Local\Programs\Python\<pythonversion>\Lib\`

- **Site-packages:**
    - `<driveletter>:\Users\<username>\AppData\Local\Programs\Python\<pythonversion>\Lib\site-packages\`

   </details>
  </div>
 </details>
 <details>
  <summary>
   <h4 style="display: inline-block">macOS</h4>
  </summary>

If you're browsing this page via a macOS session it will automatically give you a download link for macOS.

- https://www.python.org/downloads/

Alternatively, use this link instead and click on any of the "macOS 64-bit universal2 installer" links to download the version you want.

- https://www.python.org/downloads/macos/

<div style="margin-left: 1em;">
 <details>
  <summary>
   <h4 style="display: inline-block">Notes</h4>
  </summary>

- **Install directory**:
    - `/Library/Frameworks/Python.framework/Versions/<pythonversion>/`

- **Executables**:
    - `/Library/Frameworks/Python.framework/Versions/<pythonversion>/bin/`

- **Libraries**:
    - `/Library/Frameworks/Python.framework/Versions/<pythonversion>/lib/<pythonversion>/`

- **core modules**:
    - `/Library/Frameworks/Python.framework/Versions/<pythonversion>/lib/<pythonversion>/lib-dynload/`

- **Site-packages (for third-party modules)**:
    - `/Library/Frameworks/Python.framework/Versions/<pythonversion>/lib/<pythonversion>/site-packages/`

 </details>
</div>
 </details>
</div>

### 2. Edit System Paths - Windows Only

<div style="margin-left: 2em;">

All other operating system should automatically create a system link upon install, thus Windows is the only operating system where this step is necessary, you can skip it on all others.

- Type `Advanced System Settings` into Windows' primary search bar and open it

- Find the tab labeled `Advanced`.

- At the bottom click the button labeled `Environment Variables...`

- Click "Edit" on the entry labeled `path`

 <div style="margin-left: 3em;">
  <details>
   <summary>
    <h4 style="display: inline-block">Notes - <code>System variables</code> vs <code>User variables for &lt;<em>username</em>&gt;</code></h4>
   </summary>
   <div style="margin-left: 1em;">

One `path` entry can be found under `User variables for <username>`, the other entry can be found under `System variables`

If you edit `User variables for <username>`, then only the current user will have access to the python command on this computer.

However, if you edit the entry under `System variables` every user on this computer will have access to the python command.

Additionally, if you have python installed in `<driveletter>:\Users\<username>\AppData\Local\Programs\Python\<pythonversion>\`, you may or may not **have** to use the `User variables for <username>` and not `System variables` instance of `path`. I recommend keeping this consistent just in case. Windows can be a pain in the ass with some of the most benign things imaginable, so consistency should ensure maximum compatibility in any future Windows updates.

I haven't tested it, but it might be possible that if you have python installed on a user path instead of system path, setting this in the System variables might not work for other logged in Windows users.

   </div>
  </details>
 </div>

- Add a new entry that leads to the path of your python install. Typically this will be one of the following:
    - `<driveletter>:\Users\<username>\AppData\Local\Programs\Python\<pythonversion>\`
    - `<driveletter>:\Program Files\<pythonversion>\`
    - `<driveletter>:\Program Files (x86)\<pythonversion>\`

- Next add the `\Scripts\` folder as another entry in `paths`, it should be a direct sub directory of the directory you just added i.e. one of the following:
    - `<driveletter>:\Users\<username>\AppData\Local\Programs\Python\<pythonversion>\Scripts\`
    - `<driveletter>:\Program Files\<pythonversion>\Scripts\`
    - `<driveletter>:\Program Files (x86)\<pythonversion>\Scripts\`

 <div style="margin-left: 3em;">
  <details>
   <summary>
    <h4 style="display: inline-block">Notes</h4>
   </summary>
   <div style="margin-left: 1em;">

In some cases, this `\Scripts\` folder may not yet exist but it eventually will after you install `pip` in a step below.

   </div>
  </details>
 </div>

- Click OK to close and save the `Edit environment variable` window
- Then click OK again on the `Environment Variables` window.
- Now click OK again on the `System Properties` window.
- Just keep clicking OK until all the windows that have an "OK" button are closed. But they probably already were by the previous OK.

</div>

### 3. Test if Python is Installed Correctly (Optional But Recommended)

<div style="margin-left: 2em;">

- Open a new CMD prompt or Terminal.

 <div style="margin-left: 3em;">
  <details>
   <summary>
    <h4 style="display: inline-block">Notes</h4>
   </summary>
   <div style="margin-left: 1em;">

You cannot use a CMD prompt or Terminal that was already open, it has to be one that's opened AFTER you've finished steps 1 and 2.

   </div>
  </details>
 </div>

- type: `python --version` or `python3 --version`

 <div style="margin-left: 3em;">
  <details>
   <summary>
    <h4 style="display: inline-block">Notes</h4>
   </summary>
   <div style="margin-left: 1em;">

If you check the `python` file in the folder Python was installed to, you will use whatever the Python file is named. i.e., if it's named `python3`, then use `python3` (`python3 --version`), if it's named `python`, then use `python` (`python --version`), if it's named `python219` then you'll use `python219` (`python219 --version`). Whatever the Python file is named is what you will use every time you type a `python` command.

If you receive the following message (Windows Only): "Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases."

- Type `Manage app execution aliases` into windows' main search bar and open it.
- Find any entries that have python listed and disable/set them all to off.
- Now start an entirely new CMD instance and try typing `python --version` into it. It **SHOULD** work now.

   </div>
  </details>
 </div>
</div>

### 4. Install pip

<div style="margin-left: 2em;">

Run this command:

 ```sh
 python -m ensurepip --upgrade
```

 <div style="margin-left: 1em;">
  <details>
   <summary>
    <h4 style="display: inline-block">Notes</h4>
   </summary>
   <div style="margin-left: 1em;">

The `/Scripts/` folder should automatically be created after running that command. You can navigate to that folder and check the pip files. Whatever they are named, that's the command you use in your `CMD` or `Terminal` when executing `pip`.

In my case, on Windows, I have 2 pip exes in that folder
- `pip3.13.exe`
- `pip3.exe`

This means I can run pip's list command either of the following ways:

```sh
pip3 list
```

```sh
pip3.13 list
```

This command will show you what's currently installed through `pip`
If it's all a fresh new install, `pip` is likely going to be the only thing that shows up, but it's fine if other things are already installed. Just note that `pytest-blender` could require specific versions of other packages and you may need to run `pip3 uninstall <packagename>` on every conflicting package before `pytest-blender` installs correctly. Or it could install just fine. i.e.: downgrading could be a problem and you'd be better off just uninstalling versions of packages that are too high or low and not supported. BUT, note that this could cause other packages that rely on similar dependencies to stop running correctly. I'm only showing you how to set up an environment specifically for testing `OrthoScale219`.

| Package | Version |
|---------|---------|
| pip     | 25.2    |

   </div>
  </details>
 </div>
</div>

### 5. Install pytest-blender

<div style="margin-left: 2em;">

Run this command:

```sh
pip3 install --upgrade pytest-blender
```

 <div style="margin-left: 1em;">
  <details>
   <summary>
    <h4 style="display: inline-block">Notes</h4>
   </summary>
   <div style="margin-left: 1em;">

If you now run `pip3 list` again, you will probably notice these additional packages have been installed:

| Package        | Version |
|----------------|---------|
| colorama       | 0.4.6   |
| iniconfig      | 2.1.0   |
| packaging      | 25.0    |
| pluggy         | 1.6.0   |
| Pygments       | 2.19.2  |
| pytest         | 8.4.1   |
| pytest-blender | 3.0.7   |

   </div>
  </details>
 </div>
</div>

### 6. Download and Install Blender

<div style="margin-left: 2em;">

Choose any of the download methods for your operating system. Note the directories for your install method:

 <details>
  <summary>
   <h4 style="display: inline-block">Linux</h4>
  </summary>

- https://www.blender.org/download/

    Default install directories:

    - `~/<blenderversion>/`
    - `/usr/local/<blenderversion>/`
    - `/opt/<blenderversion>/`

- https://store.steampowered.com/app/365670/Blender/

    Default install directory:

    - `~/.steam/steam/steamapps/common/Blender/`

- https://snapcraft.io/blender

    Default install directory:

    - `/snap/blender/current/`

- https://flathub.org/apps/org.blender.Blender

    Default install directories:

    - `~/.local/share/flatpak/app/org.blender.Blender/current/active/files/bin/`
    - `/var/lib/flatpak/app/org.blender.Blender/current/active/files/bin/`

- Or via Terminal:

    - Ubuntu/Debian

        ```bash
        apt install blender
        ```

    - Fedora

        ```bash
        dnf install blender
        ```

    - Arch

        ```bash
        pacman -S blender
        ```

    Default install directory:

    - `/usr/share/blender/<blenderversion>/`

 </details>
 <details>
  <summary>
   <h4 style="display: inline-block">Windows</h4>
  </summary>

- https://apps.microsoft.com/detail/9pp3c07gtvrh

    Default install directory:

    - `<driveletter>:\Program Files\WindowsApps\<blenderversion>\`

- https://www.blender.org/download/

    Default install directory:

    - `<driveletter>:\Program Files\Blender Foundation\<blenderversion>\`

- https://store.steampowered.com/app/365670/Blender/

    Default install directory:

    - `<driveletter>:\Program Files (x86)\Steam\steamapps\common\Blender\`

 </details>
 <details>
  <summary>
   <h4 style="display: inline-block">macOS</h4>
  </summary>

- https://www.blender.org/download/

    Default install directory:

    - `/Applications/Blender.app/Contents/MacOS/`

- https://store.steampowered.com/app/365670/Blender/

    Default install directory:

    - `~/Library/Application Support/Steam/steamapps/common/Blender/Blender.app/Contents/MacOS/`

 </details>
</div>

### 7. Install pip to Blender's Python Runtime

<div style="margin-left: 2em;">

Run the following command based on your operating system. Change the path within the command to match the path of your Blender install from the previous step, appending `blender.exe` if using `Windows`. If using `Linux` or `macOS` then append `blender` to the path.

Don't forget to use your actual path and not the placeholder paths I have provided.

## Windows

```bat
for /f "delims=" %i in ('pytest-blender --blender-executable "<blenderexecutable>"') do set "blender_python=%i"
```

```bat
"%blender_python%" -m pip install pytest
```

## Linux or macOS

```bash
blender_python=$(pytest-blender --blender-executable "<blenderexecutable>")
```

```bash
"$blender_python" -m pip install pytest
```

</div>

### 8. Download OrthoScale219 Source

<div style="margin-left: 2em;">

https://github.com/sa-Lowell/OrthoScale219

**IMPORTANT**:

Regardless of how you download the source, the parent folder must be named `/ortho_scale_219/`

</div>

### 9. Run your Test

<div style="margin-left: 2em;">

cd to the `/ortho_scale_219/` folder:

```sh
cd ".../ortho_scale_219/"
```

Then up one directory (Essentially you want to navigate to the parent folder of `/ortho_scale_219/`):

```sh
cd ..
```

Run either of the following commands. The first one runs without output, the second one will output the print statements inside of the test files.

```sh
pytest "ortho_scale_219/tests/" --blender-executable "<blenderexecutable>" --blender-addons-dirs "<orthoscale219parent>"
```

```sh
pytest "ortho_scale_219/tests/" -s --blender-executable "<blenderexecutable>" --blender-addons-dirs "<orthoscale219parent>"
```

 <div style="margin-left: 1em;">
  <details>
   <summary>
    <h4 style="display: inline-block">Notes - Ignoring Other Packages Found in Parent Directory</h4>
   </summary>
   <div style="margin-left: 1em;">

If you have multiple python package folders within `/ortho_scale_219/`'s parent folder you might notice all of them are included when running the above test commands. If you only want `/ortho_scale_219/` to be tested then do the following before running the test command:

- In the `/ortho_scale_219/tests/conftest.py` file replace this line:

    ```python
    #addons_ids = [addon_name],
    ```

    with this line:

    ```python
    addons_ids = [addon_name],
    ```

- Next, in that same file, `/ortho_scale_219/tests/conftest.py`, replace this line:

    ```python
    #addon_name = os.path.basename(repo_root)
    ```

    with this line:

    ```python
    addon_name = os.path.basename(repo_root)
    ```

Essentially all you will do is remove the `#` on each of those two lines.

- Next, run this command to find where `pytest-blender` is installed:

    ```sh
    pip show pytest-blender
    ```

    That command shows the parent folder of `pytest-blender`.

- Now, relative to that folder, locate this file: `...\pytest_blender\run_pytest.py`.

- Open the file and replace this line of code:

    ```python
    addons_to_zipify = list(filter(lambda a: a in addons_ids, addons))
    ```

    with this line of code:

    ```python
    addons_to_zipify = list(filter(lambda a: a in addons_ids, addons_to_zipify))
    ```

It's unfortunate that these two lines have to be replaced in `run_pytest.py`. However, bugs like this are easy enough to miss and as of writing this I do not believe the dev is aware of it. Perhaps by the time you are using `pytest-blender` it will have already been fixed.

   </div>
  </details>
 </div>
</div>

See root [README.md](../README.md) for project overview.