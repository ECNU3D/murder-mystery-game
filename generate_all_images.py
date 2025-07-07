
import os
import subprocess
import sys
import argparse

# A dictionary to hold all theme configurations.
THEMES = {
    "mnfy": {
        "folder": "码农风云-谁是作弊者",
        "scripts": {
            "05_赵敏.md": {"prompt": "A powerful and elegant female HR director in her 40s, wearing a sharp business suit. Her expression is stern and uncompromising. Portrait, photorealistic, strong character.", "filename": "zhao_min.png"},
            "07_孙悦.md": {"prompt": "A young, eager and slightly nervous-looking female intern, holding a laptop and a cup of coffee. She looks like she is trying hard to make a good impression. Portrait, bright and clean style, realistic.", "filename": "sun_yue.png"}
        },
        "clues": {}
    }
}

def run_command(command, description=""):
    """Runs a command and handles errors."""
    print(f"Executing: {description}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print("Error:", result.stderr.strip(), file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}", file=sys.stderr)
        print(e.stdout.strip(), file=sys.stderr)
        print(e.stderr.strip(), file=sys.stderr)
        return False

def process_images(theme_config, venv_python, target):
    """Processes images for a given theme and target."""
    folder = theme_config['folder']
    
    items_to_process = {}
    if target in ['scripts', 'all']:
        items_to_process.update(theme_config.get('scripts', {}))
    if target in ['clues', 'all']:
        items_to_process.update(theme_config.get('clues', {}))

    for item_name, details in items_to_process.items():
        output_dir = os.path.join(folder, 'images')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_path = os.path.join(output_dir, details['filename'])
        
        generation_script = "generate_imagen4.py"
        if not os.path.exists(generation_script):
            print(f"Error: Generation script '{generation_script}' not found.", file=sys.stderr)
            return

        command = [
            venv_python,
            generation_script,
            "--prompt", details["prompt"],
            "--output_path", output_path
        ]
        run_command(command, f"Generate image for {details['filename']}")

def main():
    parser = argparse.ArgumentParser(description="Generate images for murder mystery scripts using Imagen 4.")
    parser.add_argument("--theme", required=True, choices=THEMES.keys(), help="The theme to process.")
    parser.add_argument("--target", required=True, choices=['scripts', 'clues', 'all'], help="The target to process: 'scripts', 'clues', or 'all'.")
    args = parser.parse_args()

    theme_config = THEMES.get(args.theme)
    if not theme_config:
        print(f"Error: Theme '{args.theme}' not found in configuration.", file=sys.stderr)
        sys.exit(1)

    venv_python = os.path.join(".venv", "bin", "python")
    if not os.path.exists(venv_python):
        print(f"Error: Could not find Python executable at '{venv_python}'.", file=sys.stderr)
        sys.exit(1)

    process_images(theme_config, venv_python, args.target)

    print("\nImage regeneration process complete.")

if __name__ == "__main__":
    main()
