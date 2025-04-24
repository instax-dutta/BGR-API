# Background Remover API (Flask, Rembg, Vercel-ready)

A lightweight API to remove image backgrounds and optionally replace them with a user-provided image or solid color. Includes Swagger (OpenAPI) documentation and is ready to deploy on Vercel.

## Features
- `/remove-bg` POST endpoint: Upload an image and optionally a background image or solid color.
- Returns a PNG with the background removed or replaced.
- Swagger UI at `/apidocs` for interactive API documentation.
- Designed for Vercel Python serverless deployment (under 250MB with rembg[lite]).

## Usage
### Local Development
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the server:
   ```sh
   python api/index.py
   ```
3. Access Swagger docs at [http://localhost:5000/apidocs](http://localhost:5000/apidocs)

### API Example (curl)
```sh
curl -F "image=@your_image.jpg" -F "background=@your_bg.jpg" http://localhost:5000/remove-bg --output result.png
```
Or for a solid color background:
```sh
curl -F "image=@your_image.jpg" -F "color=#00ff00" http://localhost:5000/remove-bg --output result.png
```

### Deploy to Vercel
1. Install [Vercel CLI](https://vercel.com/download) and log in.
2. Deploy:
   ```sh
   vercel --prod
   ```
3. Your API will be available at your Vercel deployment URL. Swagger docs at `/apidocs`.

## File Structure
- `api/index.py` - Main Flask API with Swagger docs and Vercel handler.
- `requirements.txt` - Minimal dependencies for <250MB deployment.
- `vercel.json` - Vercel routing/build configuration.
- `README.md` - This file.

## Notes
- Uses `rembg[lite]` for smallest model and fastest cold start on Vercel.
- For larger models or custom backgrounds, use a dedicated VM or container.
- If you encounter memory or cold start issues, consider optimizing your images before upload.

---
MIT License
