# Background Remover API (Flask, Rembg, Render-ready)

A lightweight API to remove image backgrounds and optionally replace them with a user-provided image or solid color. Includes Swagger (OpenAPI) documentation and is ready for deployment on Render, a VM, or any Ubuntu server.

## Features
- `/remove-bg` POST endpoint: Upload an image and optionally a background image or solid color.
- Returns a PNG with the background removed or replaced.
- Swagger UI at `/apidocs` for interactive API documentation.
- Designed for Render Python web service or direct Ubuntu/VM deployment.

## Usage

### Local/Server Deployment (Ubuntu, VM, or any Linux)

#### **Quickstart with Bash Script**

1. Make the script executable:
   ```sh
   chmod +x start_api.sh
   ```
2. Run the script:
   ```sh
   ./start_api.sh
   ```
- The script will:
  - Create a Python virtual environment (or activate an existing one)
  - Upgrade pip
  - Install all dependencies
  - Start the API using Gunicorn on port 10000

#### **Manual Steps**

```sh
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
gunicorn app:app --bind 0.0.0.0:10000
```

- The API will be available at [http://localhost:10000](http://localhost:10000)
- Swagger docs at [http://localhost:10000/apidocs](http://localhost:10000/apidocs)

### API Example (curl)
```sh
curl -F "image=@your_image.jpg" -F "background=@your_bg.jpg" http://localhost:10000/remove-bg --output result.png
```
Or for a solid color background:
```sh
curl -F "image=@your_image.jpg" -F "color=#00ff00" http://localhost:10000/remove-bg --output result.png
```

### Render.com Deployment
1. Ensure you have `app.py`, `requirements.txt`, and `render.yaml` in your repo root.
2. Push your code to GitHub.
3. Go to [render.com](https://render.com/), click "New Web Service", and connect your repo.
4. Render will auto-detect your Python app and deploy using Gunicorn.
5. Your API will be available at your Render deployment URL. Swagger docs at `/apidocs`.

## File Structure
- `app.py` - Main Flask API with Swagger docs.
- `requirements.txt` - Minimal dependencies for cloud or VM deployment.
- `start_api.sh` - Bash script to set up venv, install deps, and start the server.
- `render.yaml` - Render routing/build configuration.
- `README.md` - This file.

## Notes
- Uses `rembg[lite]` for smallest model and fastest cold start.
- If you encounter memory or cold start issues, consider optimizing your images before upload.
- For production, run behind a reverse proxy (nginx) or use Cloudflare Tunnel for secure public access.

---
MIT License
