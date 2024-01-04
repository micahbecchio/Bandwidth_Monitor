![Banner Placeholder](Static/bandwidth_banner.jpg)
<!-- banner -->

A simple yet powerful Python script for macOS users to monitor one's bandwidth usage effectively.

<!-- ![GIF Placeholder](Static/preview.gif)   -->
<!-- GIF. -->
<p align="center">
  <img src="Static/preview.gif" alt="animated" />
</p>

## How to Run
To use this script, simply run it with Python 3:

```bash
python3 main.py
```

## Features and Usage
- **Monitor Bandwidth:** Displays real-time network usage in the status bar (1/s).
- **Total Bandwidth:** Shows the total data used since the program was opened.
- **Scale:** Choose between Bytes, MB, or GB to display bandwidth usage.
- **Stop Monitor:** Stop current monitoring thread.

The script is designed with a focus on simplicity and efficiency, using threads to ensure smooth performance.

## Dependencies
- `rumps`: For creating macOS status bar applications.
- `psutil`: For accessing system and network usage statistics.
- `threading`: To avoid blocking the main thread.

<br><br><br><br>