from flask import Flask, request, send_file, jsonify, redirect
from rembg import remove
from PIL import Image
import io
import logging
import random
import string

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided.'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400
    color_hex = request.form.get('color')
    try:
        input_bytes = file.read()
        input_image = Image.open(io.BytesIO(input_bytes)).convert('RGBA')
        output_image = remove(input_image)
        if 'background' in request.files:
            bg_file = request.files['background']
            if bg_file.filename == '':
                return jsonify({'error': 'No background image selected.'}), 400
            try:
                bg_bytes = bg_file.read()
                bg_img = Image.open(io.BytesIO(bg_bytes)).convert('RGBA')
                bg_img = bg_img.resize(output_image.size)
                bg_img.paste(output_image, (0, 0), output_image.split()[-1])
                output_image = bg_img
            except Exception as ex:
                logging.error(f'Exception during background image processing: {ex}')
                return jsonify({'error': f'Error processing background image: {str(ex)}'}), 500
        elif color_hex:
            if color_hex.startswith('#'):
                color_hex = color_hex[1:]
            if len(color_hex) not in (6, 8):
                return jsonify({'error': 'Color must be a hex string like #RRGGBB or #RRGGBBAA.'}), 400
            try:
                rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
                alpha = int(color_hex[6:8], 16) if len(color_hex) == 8 else 255
                bg_color = (*rgb, alpha)
            except Exception:
                return jsonify({'error': 'Invalid color hex format.'}), 400
            bg = Image.new('RGBA', output_image.size, bg_color)
            bg.paste(output_image, mask=output_image.split()[-1])
            output_image = bg
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        return send_file(
            output_buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name='no-bg.png'
        )
    except Exception as e:
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500

@app.route('/fetch-image', methods=['GET'])
def fetch_image():
    style = request.args.get('style', 'random')
    # Use Unsplash Source API (no API key needed)
    # Example: https://source.unsplash.com/random/800x600/?professional
    url = f"https://source.unsplash.com/random/800x600/?{style}"
    # Option 1: Redirect user to Unsplash image (fast, no download)
    return redirect(url)
    # Option 2: Download and serve image directly (uncomment below if you want to serve the image bytes)
    # try:
    #     resp = requests.get(url)
    #     resp.raise_for_status()
    #     return send_file(io.BytesIO(resp.content), mimetype='image/jpeg', as_attachment=True, download_name=f'random-{style}.jpg')
    # except Exception as e:
    #     return jsonify({'error': f'Failed to fetch image: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found.'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
