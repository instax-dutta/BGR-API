from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io
import logging
from flasgger import Swagger, swag_from

app = Flask(__name__)
Swagger(app)

logging.basicConfig(level=logging.INFO)

@app.route('/remove-bg', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'image',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Input image file (with background)'
        },
        {
            'name': 'background',
            'in': 'formData',
            'type': 'file',
            'required': False,
            'description': 'Background image file (optional, replaces background)'
        },
        {
            'name': 'color',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Solid background color (hex, e.g., #ffffff) if no background image provided'
        }
    ],
    'responses': {
        200: {
            'description': 'Processed image as PNG',
            'content': {'image/png': {}}
        },
        400: {'description': 'Invalid input'},
        500: {'description': 'Processing error'}
    }
})
def remove_bg():
    """Remove background from image and optionally replace it with a user-provided background or color."""
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

@app.route('/')
def docs_redirect():
    return '<h2>See <a href="/apidocs">Swagger Docs</a></h2>'

app.config['SWAGGER'] = {
    'title': 'Background Remover API',
    'uiversion': 3
}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
