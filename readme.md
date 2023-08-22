# Growroom Assistant

The Growroom Assistant is your solution for indoor gardening success, providing effortless humidity management and the ideal growth environment for various plant stages. This application, designed for efficiency, operates on the PyQt framework and gives you control over dehumidifiers and air conditioners. By optimizing your plant's cultivation environment, the Growroom Assistant empowers you to create the perfect conditions for growth.

## Features

- **Easy Device Setup**: Setting up your devices is hassle-free with the Growroom Assistant. You can add device details, including IP addresses and tokens, directly within the app's user-friendly settings. To obtain the required IP addresses and tokens, use the Miio CLI cloud commands.

- **Tailored Humidity Control**: Take charge of your plant's growth journey by setting customizable humidity levels for different phases. This flexibility ensures that your plants experience optimal conditions at each stage.

- **Cooler Nighttime Environment (Upcoming)**: An exciting upcoming feature allows you to simulate cooler nighttime temperatures using air conditioners, further refining your plant's environment.

## Getting Started

### Installation

To get started, install the required dependencies from the provided `requirements.txt` file:

```shell
pip install -r requirements.txt
```

### Running the App

Launch the application by executing the following command:

```shell
python main.py
```

### Initial Setup

When configuring your devices, you have the option to add device details, including the ID, IP address, and token, directly within the app's settings. This streamlines the process and eliminates the need to manually edit the `dehumidifiers.json` file.

To obtain the necessary IP addresses and tokens for your devices, use the Miio CLI cloud commands provided by the manufacturer.

### Configuration

Tailor the application to your specific needs with these steps:

1. Access the app's settings and look for the option to add device details.

2. Alternatively, you can still modify the `dehumidifiers.json` file if you prefer to manage device information manually.

3. Adjust settings for different growth phases using the `settings.json` file or directly from the app's settings menu.

### Usage

Here's how to make the most of the Growroom Assistant:

1. Open the app and follow the prompts to configure your devices and set desired humidity levels.

2. Once configured, let the application seamlessly manage humidity levels during various growth phases.

3. Stay tuned for the upcoming feature that enables configuring air conditioners for a cooler nighttime environment, benefiting your plants.

### Debugging and Connectivity

For those intrigued by technical details, a debugging feature logs interactions to a JSON file. Additionally, within the settings, you can manually connect or disconnect operations with the dehumidifier unit. To enable these features, ensure you have the IP and token obtained from the Miio CLI. Remember, you need to obtain these details independently; the app doesn't handle this for you. Also, ensure your device is registered with the online app to access Miio CLI cloud capabilities.

## Contributing

Contributions and suggestions are enthusiastically welcomed! As a solo developer, your input is highly valuable. Feel free to submit pull requests or create issues for any encountered problems or ideas for improvements.

## License

This project is licensed under the MIT License. Refer to the `LICENSE` file in the repository for more details.