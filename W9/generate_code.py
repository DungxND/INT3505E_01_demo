import subprocess
import os

yaml_file = "api-doc.yaml"

output_dir = "./generated_code"

os.makedirs(output_dir, exist_ok=True)

result = subprocess.run(
    [
        "openapi-generator-cli",
        "generate",
        "-i",
        yaml_file,
        "-g",
        "python-flask",
        "-o",
        output_dir,
    ],
    capture_output=True,
    text=True,
)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
