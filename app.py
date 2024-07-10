from flask import Flask, request, render_template, send_file, redirect, url_for
from PIL import Image
import os
import uuid
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

def combine_images(front_image_path, back_image_path, output_image_path, border_size=10):
    try:
        front_image = Image.open(front_image_path)
        back_image = Image.open(back_image_path)
        
        if front_image.height != back_image.height:
            back_image = back_image.resize((back_image.width, front_image.height))
        
        combined_width = front_image.width + back_image.width + border_size * 3
        combined_height = max(front_image.height, back_image.height) + border_size * 2
        
        combined_image = Image.new('RGB', (combined_width, combined_height), (255, 255, 255))
        combined_image.paste(front_image, (border_size, border_size))
        combined_image.paste(back_image, (front_image.width + 2 * border_size, border_size))
        combined_image.save(output_image_path)
    except Exception as e:
        logging.error(f"Error combining images: {e}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        front_file = request.files['front_image']
        back_file = request.files['back_image']

        if front_file and back_file:
            # Generate unique filenames for the uploaded and output files
            front_filename = str(uuid.uuid4()) + "_" + front_file.filename
            back_filename = str(uuid.uuid4()) + "_" + back_file.filename
            output_filename = str(uuid.uuid4()) + "_combined.jpg"
            
            front_path = os.path.join('static', front_filename)
            back_path = os.path.join('static', back_filename)
            output_path = os.path.join('static', output_filename)
            
            front_file.save(front_path)
            back_file.save(back_path)
            
            combine_images(front_path, back_path, output_path)

            return redirect(url_for('index', combined_image=output_filename))
    except Exception as e:
        logging.error(f"Error in upload_files: {e}")
        return "Internal Server Error", 500

    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join('static', filename), as_attachment=True)
    except Exception as e:
        logging.error(f"Error in download_file: {e}")
        return "File Not Found", 404

if __name__ == '__main__':
    app.run(debug=True)
