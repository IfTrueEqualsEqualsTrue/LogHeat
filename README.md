# Temperature Logger

This project is a temperature logging system developed during the 2024 Biomedical Engineering Master Class at Grenoble INP. The system is designed to record temperature data in real-time, offering students practical experience in data acquisition, processing, and visualization, relevant to biomedical applications.

## Features
- **Real-time temperature logging**: Captures temperature data from a connected sensor.
- **Data storage**: Saves logged data for later analysis.
- **Data visualization**: Provides a graphical interface for displaying temperature trends over time.
- **Simple UI**: User-friendly interface for ease of use by non-technical users.
  
This app does not include the possibility for the MCP inputs but it can be easily tweaked in the file ```SpiInteface.py```

## Hardware Requirements
- Thermocouple sensor
- MAX31855 thermocouple conditionning circuit

## Running the Application

The main.py file is the entry point for the application. The required packages can be installed in a new virtual environment using:

```bash
pip install -r requirements.txt
```

To run the application, execute the main file using the following command:

```bash
python src/main.py
```

## Compiling

To use the app on as a standalone, it can be compiled using pyinstaller.

Use the following command to compile the app:

```bash
pyinstaller main.spec
```

This will create a dist folder containing the compiled app. Compile on the os the app should be used on.

## Contributors
Grenoble INP Biomedical Engineering Students:
- Guillaume Boulet
- Paul Ménard
- Lucie Martinal
- Guillermo Lazarin

