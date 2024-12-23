# Hardware Diagnostic Tool

A cross-platform Python tool for gathering detailed hardware information about your system, including:
- System information (OS, version, machine details)
- CPU information (cores, frequency, usage)
- Memory information (RAM and swap usage)
- Storage information (disk space and usage)
- GPU information (if available)

## Requirements
- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone or download this repository
2. Open a terminal/command prompt and navigate to the project directory
3. Install the required packages:

```bash
# On macOS/Linux:
pip3 install -r requirements.txt

# On Windows:
pip install -r requirements.txt
```

## Usage

### On macOS/Linux:
```bash
./hardware_info.py
```
or
```bash
python3 hardware_info.py
```

### On Windows:
```bash
python hardware_info.py
```

## Output
The tool will display detailed information about your system's hardware in a formatted table, including:
- Operating system details
- CPU specifications and usage
- Memory (RAM) usage and availability
- Storage devices and their usage
- GPU information (if available)

## Troubleshooting

### Permission Denied (macOS/Linux)
If you get a "Permission denied" error when trying to run `./hardware_info.py`, make the file executable:
```bash
chmod +x hardware_info.py
```

### Missing Dependencies
If you get import errors, ensure you've installed the required packages:
```bash
pip install -r requirements.txt
```

### GPU Information Not Available
GPU information requires compatible graphics drivers and may not be available on all systems. The tool will continue to function and display other system information even if GPU data cannot be retrieved.