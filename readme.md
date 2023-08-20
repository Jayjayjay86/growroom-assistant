# Growroom Assistant
The Growroom Assistant is an application designed to assist indoor gardeners in managing humidity levels and environmental conditions during various growing phases. It utilizes the PyQt framework along with the tinytuya and python-miio libraries to control dehumidifiers and air conditioners, ensuring optimal conditions for plant growth.

## Features
Automatic recognition of dehumidifiers and air conditioners using the provided dehumidifiers.json file.
Manual configuration of devices through settings files.
Customizable humidity levels for different growing phases.
Future feature: Nighttime temperature simulation using air conditioners.
## Getting Started
### Installation:
Install the required dependencies using the provided requirements file:

```pip install -r requirements.txt```
### Running the App:
To start the application, execute:


```python main.py```

### Initial Setup:

If no dehumidifiers are listed in the dehumidifiers.json file, the app's settings will prompt you to provide the details of an active unit.
Once configured, the app will control the active devices according to the settings.
Configuration:

Modify the dehumidifiers.json file to include dehumidifiers' id, ip, token, and active status.
Adjust growing phase settings using the settings.json file or through the settings menu in the app.
Usage:

Run the app and follow prompts to set up devices and desired humidity levels.
Allow the app to manage humidity levels throughout different growing phases.

Future feature: Configure air conditioners to simulate nighttime temperature changes.

## Contributing
Contributions and suggestions are welcome! Feel free to submit pull requests or issues if you encounter problems or have ideas for improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
