# VS Code settings for this workspace

This folder (`openHASP/`) is synced via Synology Drive between a Windows machine and a
Linux machine. VS Code workspace settings (`.vscode/settings.json`) are a single file, so
they can't automatically switch values based on the OS you're currently using — whichever
machine last edited `settings.json` "wins" for the other one too, unless you swap it.

## Files

| File | Purpose |
| --- | --- |
| `settings.json` | The file VS Code actually reads. Always holds whichever OS's values are currently active. |
| `settings.windows.json` | Reference copy of the settings to use on Windows. |
| `settings.linux.json` | Reference copy of the settings to use on Linux. |

## Switching machines

When you move from one OS to the other, copy the matching reference file over
`settings.json` before opening/using this workspace:

**On Windows (PowerShell):**
```powershell
Copy-Item .vscode\settings.windows.json .vscode\settings.json -Force
```

**On Linux:**
```bash
cp .vscode/settings.linux.json .vscode/settings.json
```

If you change a setting, update both `settings.json` and the matching `settings.*.json`
reference file so the other OS's copy doesn't go stale.

## Current settings

### `openhasp.editor.iconFont`

Absolute path to `fonts/openhasp-icons.ttf`, used by the
[openHASP Page Editor](https://marketplace.visualstudio.com/items?itemName=prasenpalvankar.openhasp-editor)
extension to render `\uXXXX` icon glyphs on the design canvas exactly as they appear on the
device. Without a correct, OS-appropriate absolute path here, icons render as empty boxes.

| OS | Path |
| --- | --- |
| Windows | `c:/Users/gerar/SynologyDrive/ESPHome/openHASP/fonts/openhasp-icons.ttf` |
| Linux | `/home/gerard/ESPHome/openHASP/fonts/openhasp-icons.ttf` |

If `fonts/openhasp-icons.ttf` is missing or out of date (e.g. after updating
`fonts/md-icons.json` or `fonts/materialdesignicons-webfont.ttf`), rebuild it with:

```
python fonts/build_shifted_icon_font.py
```
