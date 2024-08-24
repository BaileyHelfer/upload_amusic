
# upload_amusic

This repository contains a Python project that automates the upload process for music files. The project uses a combination of Python, AppleScript, and web technologies to streamline the music uploading process. Below is an overview of the project structure and how to get started.

## Project Structure

- **main.py**: The main script that drives the application.
- **config.yaml**: Configuration file for storing application settings.
- **static/**: Directory containing static assets such as CSS and JavaScript files.
- **templates/**: Directory containing HTML templates for the web interface.
- **script.applescript**: AppleScript file used for automating tasks on macOS.
- **requirements.txt**: Lists the Python dependencies required for the project.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/BaileyHelfer/upload_amusic.git
   cd upload_amusic
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Configure the application by editing the `config.yaml` file.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Access the web interface by navigating to `http://localhost:5000` in your browser.

## Contributing

Feel free to fork this project, submit issues, or make pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License.
