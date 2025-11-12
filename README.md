Wiz Light Change — tiny Tkinter GUI for WiZ smart bulbs

This is a small, beginner-level Python project I put together while I was essentially bored. It’s a simple desktop app that finds a WiZ smart bulb on your local network and lets you change its color or power state from an easy Tkinter GUI.

Features
- Auto-discovery of a WiZ bulb on your network (first one found)—Will try to implement multi-bulb support in the future.
- On/Off controls
- One-click Red, Green, Blue presets
- Custom color via RGB sliders or a color picker dialog
- Basic logging of actions and network discovery

How it works
- The app uses the pywizlight library to talk to WiZ bulbs on your LAN.
- On start, it discovers bulbs by broadcasting over your active network interfaces.
- The GUI (Tkinter) exposes buttons for presets and a color picker to set any RGB color.
- Actions are logged to files for simple troubleshooting.

Project structure
- main.py — Tkinter GUI and user interactions
- commands/cmds.py — Bulb discovery and control (async functions with pywizlight)
- Images/color-picker.png — Screenshot/illustration of the color picker
- logs/actions.log — App action logs (created at runtime)
- commands/command_logs/connection.log — Discovery/connection logs (created at runtime)
- bulbconf.txt — Last retrieved bulb configuration (written at runtime)

Requirements
- OS: Windows (current code paths and registry lookups are Windows-oriented)
- Python: 3.10+ (tested on a Python 3.13 environment)
- Packages:
  - pywizlight
  - netifaces
  - colorama
  - tkinter (comes with standard Python on Windows)

Install
1) (Optional but recommended) Create and activate a virtual environment
   - Windows PowerShell
     ```
     py -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
2) Install dependencies
   ```
   pip install pywizlight netifaces colorama
   ```

Run
```
python main.py
```

Usage
- When the app starts, it will attempt to discover a WiZ bulb on your network.
- Use the buttons:
  - On / Off to toggle power
  - Red / Green / Blue for one-click colors
  - Color Picker to choose any color via:
    - Pick Color: native color dialog
    - RGB sliders: fine-tune values, then Confirm


Configuration notes
- Discovery: The app broadcasts over each active IPv4 interface to find bulbs. Make sure your PC is on the same network (Wi‑Fi/LAN) as the bulb.
- MAC address: In `commands/cmds.py`, the `bulb_config()` function passes a fixed example MAC to `wizlight(...)`. If your bulb has a different MAC or you control multiple bulbs, you may want to remove or update that parameter to avoid mismatches.
- Single bulb assumption: The app uses the first discovered bulb by default.

Logs and diagnostics
- GUI actions: `logs/actions.log`
- Discovery/connection: `commands/command_logs/connection.log`
- Bulb configuration snapshot: `bulbconf.txt`

Known limitations (future improvement ideas)
- Windows-specific: network interface lookups use Windows registry via `winreg` and `netifaces`.
- Single-device focus: the first discovered bulb is used; no UI to pick among multiple bulbs yet.
- Blocking calls per action: the GUI triggers `asyncio.run(...)` for each command; a more advanced version would keep a running loop or use threads for smoother responsiveness.

Troubleshooting
- “No bulbs found”: Ensure the bulb is powered on and connected to the same network as your PC. Verify firewall settings allow local broadcast/UDP traffic.
- Multiple networks/adapters: If you have VPNs or virtual adapters, discovery might scan the wrong segment first. Try disconnecting extra adapters or ensure the active adapter is on the bulb’s subnet.
- Permissions: Running from a location where the app can write logs is required (project folder).

Credits
- Built with pywizlight for WiZ bulb control.
- Made for learning and fun tbh.

License
- No explicit license provided. Feel free to explore and learn from the code.
