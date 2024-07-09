from flask import Flask, request, render_template, send_file, redirect, url_for
from PIL import Image
import os
import uuid

app = Flask(__name__)

def combine_images(front_image_path, back_image_path, output_image_path, border_size=10):
    # Open the front and back images
    front_image = Image.open(front_image_path)
    back_image = Image.open(back_image_path)
    
    # Ensure both images have the same height
    if front_image.height != back_image.height:
        back_image = back_image.resize((back_image.width, front_image.height))
    
    # Calculate the dimensions of the combined image
    combined_width = front_image.width + back_image.width + border_size * 3
    combined_height = max(front_image.height, back_image.height) + border_size * 2

    # Create a new image with a white background
    combined_image = Image.new('RGB', (combined_width, combined_height), (255, 255, 255))
    
    # Paste the images with a border
    combined_image.paste(front_image, (border_size, border_size))
    combined_image.paste(back_image, (front_image.width + 2 * border_size, border_size))
    
    # Save the combined image
    combined_image.save(output_image_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
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
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join('static', filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
