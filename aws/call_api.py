import subprocess
import os
import json

PATH_TO_IMAGE = "../images/2.jpg"
PATH_OUTPUT = "output.json"
AWS_TEXTRACT_FOLDER = "aws-textract"


def run_textract_commands(path_to_image=PATH_TO_IMAGE):
    if not os.path.exists(AWS_TEXTRACT_FOLDER):
        print(f"Error: The folder '{AWS_TEXTRACT_FOLDER}' does not exist.")
        return
    
    os.chdir(AWS_TEXTRACT_FOLDER)
    
    try:
        print("Converting the image to Base64...")
        subprocess.run(
            ["base64", "-i", path_to_image, "-o", "temp_base64.txt"],
            check=True
        )
        print("Conversion completed. Base64 file saved as 'temp_base64.txt'.")
        
        print("Reading the content of 'temp_base64.txt'...")
        with open("temp_base64.txt", "r") as f:
            base64_encoded = f.read().strip()

        print("Creating a temporary JSON input file for AWS Textract...")
        document_json = {
            "Bytes": base64_encoded
        }
        with open("document.json", "w") as json_file:
            json.dump(document_json, json_file)

        print("Running the AWS Textract command...")
        aws_command = [
            "aws", "textract", "analyze-document",
            "--document", "file://document.json",
            "--feature-types", "LAYOUT",
            "--region", "us-east-1"
        ]
        
        with open(PATH_OUTPUT, "w") as output_file:
            subprocess.run(aws_command, stdout=output_file, check=True)
        
        print(f"Analysis completed. Results saved in {PATH_OUTPUT}.")

    except subprocess.CalledProcessError as e:
        print(f"Error while executing the command: {e}")
    except Exception as e:
        print(f"General error: {e}")
    finally:
        # Cleanup temporary files
        print("Cleaning up temporary files...")
        if os.path.exists("temp_base64.txt"):
            os.remove("temp_base64.txt")
            print("Removed 'temp_base64.txt'.")
        if os.path.exists("document.json"):
            os.remove("document.json")
            print("Removed 'document.json'.")


if __name__ == "__main__":
    run_textract_commands()
