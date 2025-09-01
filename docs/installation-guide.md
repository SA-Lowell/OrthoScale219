# Installation Guide

Follow these methods to install OrthoScale219. No external dependencies beyond Blender's built-in modules (e.g., bpy, mathutils). The add-on uses Python 3.x features available in Blender.

## Method 1: Install from ZIP File (Easy)

1. **Download the Add-On**:
   - Download the ZIP file containing the add-on.

2. **Install in Blender**:
   - `Open Blender`.
   - Go to `Edit > Preferences > Add-ons`.
   - Click the `downward facing arrow` on the `top right`.
   - Click `Install from Disk...` and select the `ZIP file`.
   - Enable the add-on by `checking the box next to OrthoScale219 (If not already checked)`.

3. **Verify Installation**:
   - The panel for this plugin should appear in `Properties > Render > OrthoScale219`.
   - If not visible, follow the 2nd step from **Install in Blender** and search for `OrthoScale219` in the Add-ons search bar and ensure it's enabled/checked then verify the 1st step from `Verify Installation`.

## Method 2: Manually Install from Files (Annoying)

1. **Download the Files**:
   - Download the `__init__.py` file.
   - Download the `blender_manifest.toml` file.

2. **Locate Install Folders**:

   Locate Blender's `user_default` folder.

   - **Linux**:
     ```bash
     ~/.config/blender/<version>/extensions/user_default/
     ```

   - **Windows**:
     ```bash
     %APPDATA%\Blender Foundation\Blender\<version>\extensions\user_default\
     ```

   - **macOS**:
     ```bash
     /Users/<username>/Library/Application Support/Blender/<version>/extensions/user_default/
     ```

   - Replace `<version>` with `your Blender Version`
      - ie: `4.5` = `~/.config/blender/4.5/extensions/user_default/`

   - Replace `<username>` with `your Username`
      - Only applicable on `macOS`.
      - ie: `salowell` = `/Users/salowell/Library/Application Support/Blender/<version>/extensions/user_default/`
      - ie: Full URI = `/Users/salowell/Library/Application Support/Blender/4.5/extensions/user_default/`

   **Note**: This is one of two locations that blender installs add-ons. This folder is specifically for add-ons that come paired with a `blender_manifest.toml` (Which this add-on does come with). The other folder (The location of which is not mentioned anywhere in this ReadMe. But you have probably seen this other folder in various other Blender add-on install instructions.) is for add-ons that use `bl_info` instead of a `blender_manifest.toml`.

3. **Create `ortho_scale_219` Folder**:

   Create a folder named `ortho_scale_219` in the `user_default` directory. It should now look like one of the following based on your operating system:

   - **Linux**:
     ```bash
     ~/.config/blender/<version>/extensions/user_default/ortho_scale_219/
     ```

   - **Windows**:
     ```bash
     %APPDATA%\Blender Foundation\Blender\<version>\extensions\user_default\ortho_scale_219\
     ```

   - **macOS**:
     ```bash
     /Users/<username>/Library/Application Support/Blender/<version>/extensions/user_default/ortho_scale_219/
     ```

4. **Add OrthoScale219 Files to the `ortho_scale_219` folder**:

   Add the `__init__.py` and `blender_manifest.toml` to the `ortho_scale_219` folder. It should now have the following structure:

   - **__init__.py**:
     ```bash
     /extensions/user_default/ortho_scale_219/__init__.py
     ```

   - **blender_manifest.toml**:
     ```bash
     /extensions/user_default/ortho_scale_219/blender_manifest.toml
     ```

   **Note**: Structures are left truncated to the `extensions` directory in these two examples. The full path before the `extensions` directory still remains exactly as it is in Step 3 for your operating system.

5. **Activate in Blender**:
   - Open Blender.
   - Go to `Edit > Preferences > Add-ons`.
   - Click the `downward facing arrow` on the `top right`.
   - Click `Refresh Local`
   - In the `Search Add-ons` type `OrthoScale219` and it should show up in the list below.
   - Enable the add-on by checking the box next to `OrthoScale219` (If not already checked).

6. **Verify Installation**:
   - The panel for this plugin should appear in `Properties > Render > OrthoScale219`.
   - If not visible, follow the 2nd step from `Activate in Blender` and search for `OrthoScale219` in the Add-ons search bar and ensure it's enabled/checked then verify the 1st step from `Verify Installation`.

**Note**: No external dependencies are required beyond Blender's built-in modules (e.g., bpy, mathutils). The add-on uses Python 3.x features available in Blender.

Return to [main README](../README.md) or [docs index](README.md).