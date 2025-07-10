from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import random
import string
import io
import base64
from typing import List, Dict, Optional
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
IMAGE_SIZE = (400, 400)
FONT_SIZE = 180
TEXT_COLOR = "white"
OUTPUT_DIR = "generated_images"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Linux
# Alternative font paths for different systems
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
    "/System/Library/Fonts/Arial.ttf",  # macOS
    "C:/Windows/Fonts/arial.ttf",  # Windows
    "arial.ttf"  # Fallback
]

# Spiritual and cultural color palette for MyTempleYatra
BACKGROUND_COLORS = [
    "#FF9933",  # Saffron - Sacred Hindu color
    "#FFD700",  # Gold - Divine and auspicious
    "#A569BD",  # Purple - Spirituality and wisdom
    "#1ABC9C",  # Turquoise - Tranquility and peace
    "#2C3E50",  # Dark blue - Depth and devotion
    "#E74C3C",  # Red - Energy and power
    "#F39C12",  # Orange - Warmth and enthusiasm
    "#27AE60",  # Green - Growth and harmony
    "#8E44AD",  # Deep purple - Mysticism
    "#D35400",  # Dark orange - Vitality
    "#2980B9",  # Blue - Trust and stability
    "#C0392B",  # Dark red - Passion and strength
]

class ProfileImageGenerator:
    def __init__(self):
        self.font = self._load_font()
        self._ensure_output_directory()
    
    def _load_font(self):
        """Load font from available paths"""
        for font_path in FONT_PATHS:
            try:
                return ImageFont.truetype(font_path, FONT_SIZE)
            except OSError:
                continue
        
        # Fallback to default font
        logger.warning("Could not load custom font, using default")
        return ImageFont.load_default()
    
    def _ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
    
    def extract_initials(self, first_name: str, last_name: str) -> str:
        """Extract 2-letter uppercase initials from first and last name"""
        if not first_name or not last_name:
            raise ValueError("Both first_name and last_name are required")
        
        # Clean and extract initials
        first_initial = first_name.strip()[0].upper()
        last_initial = last_name.strip()[0].upper()
        
        return first_initial + last_initial
    
    def create_image(self, initials: str, variant: int, bg_color: str) -> Image.Image:
        """Create a profile image with given initials and background color"""
        # Create blank image
        img = Image.new("RGB", IMAGE_SIZE, color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Get text dimensions for centering
        bbox = draw.textbbox((0, 0), initials, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position to center text
        x = (IMAGE_SIZE[0] - text_width) / 2
        y = (IMAGE_SIZE[1] - text_height) / 2 - 20  # Slight upward adjustment
        
        # Draw initials
        draw.text((x, y), initials, fill=TEXT_COLOR, font=self.font)
        
        return img
    
    def generate_variants(self, initials: str, num_variants: int = 3) -> List[Dict]:
        """Generate multiple variants of profile images for given initials"""
        variants = []
        
        # Create directory for this initial combination
        initials_dir = os.path.join(OUTPUT_DIR, initials)
        os.makedirs(initials_dir, exist_ok=True)
        
        # Use different colors for each variant
        colors = random.sample(BACKGROUND_COLORS, min(num_variants, len(BACKGROUND_COLORS)))
        
        for variant in range(1, num_variants + 1):
            bg_color = colors[variant - 1]
            
            # Create image
            img = self.create_image(initials, variant, bg_color)
            
            # Save image
            filename = f"{initials}_variant{variant}.png"
            filepath = os.path.join(initials_dir, filename)
            img.save(filepath)
            
            variants.append({
                'variant': variant,
                'filename': filename,
                'filepath': filepath,
                'bg_color': bg_color,
                'url': f"/image/{initials}/{filename}"
            })
        
        return variants
    
    def get_random_variant(self, initials: str) -> Optional[Dict]:
        """Get a random variant for given initials"""
        initials_dir = os.path.join(OUTPUT_DIR, initials)
        
        if not os.path.exists(initials_dir):
            # Generate variants if they don't exist
            variants = self.generate_variants(initials)
            return random.choice(variants)
        
        # Get existing variants
        files = [f for f in os.listdir(initials_dir) if f.endswith('.png')]
        if not files:
            variants = self.generate_variants(initials)
            return random.choice(variants)
        
        # Return random existing variant
        random_file = random.choice(files)
        variant_num = random_file.split('_variant')[1].split('.')[0]
        
        return {
            'variant': int(variant_num),
            'filename': random_file,
            'filepath': os.path.join(initials_dir, random_file),
            'url': f"/image/{initials}/{random_file}"
        }

# Initialize generator
generator = ProfileImageGenerator()

@app.route('/', methods=['GET'])
def index():
    """Root endpoint - API information"""
    return jsonify({
        'service': 'MyTempleYatra Profile Image Generator API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'generate': '/generate',
            'generate_variants': '/generate-variants',
            'bulk_generate': '/bulk-generate',
            'colors': '/colors',
            'stats': '/stats',
            'image_serve': '/image/<initials>/<filename>',
            'image_base64': '/image-base64/<initials>/<filename>'
        },
        'documentation': 'Send POST requests to /generate with JSON: {"first_name": "John", "last_name": "Doe"}'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'MyTempleYatra Profile Image Generator',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/generate', methods=['POST'])
def generate_profile_image():
    """Generate profile image for user registration"""
    try:
        # More robust JSON parsing
        data = None
        
        # Try to get JSON data
        try:
            data = request.get_json()
        except Exception as json_error:
            logger.error(f"JSON parsing error: {json_error}")
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        if not data:
            # Try to get data from form or raw data as fallback
            try:
                import json as json_module
                raw_data = request.get_data(as_text=True)
                logger.info(f"Raw request data: {raw_data}")
                data = json_module.loads(raw_data)
            except Exception as fallback_error:
                logger.error(f"Fallback parsing error: {fallback_error}")
                return jsonify({'error': 'No valid JSON data provided'}), 400
        
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        if not first_name or not last_name:
            return jsonify({
                'error': 'Both first_name and last_name are required'
            }), 400
        
        # Extract initials
        initials = generator.extract_initials(first_name, last_name)
        
        # Get random variant
        variant = generator.get_random_variant(initials)
        
        if not variant:
            return jsonify({'error': 'Failed to generate image'}), 500
        
        response = {
            'success': True,
            'user_info': {
                'first_name': first_name,
                'last_name': last_name,
                'initials': initials
            },
            'image': variant,
            'message': f'Profile image generated successfully for {first_name} {last_name}'
        }
        
        logger.info(f"Generated profile image for {first_name} {last_name} (initials: {initials})")
        return jsonify(response)
        
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error generating profile image: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/generate-variants', methods=['POST'])
def generate_variants():
    """Generate multiple variants for given initials"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        num_variants = data.get('num_variants', 3)
        
        if not first_name or not last_name:
            return jsonify({
                'error': 'Both first_name and last_name are required'
            }), 400
        
        if not isinstance(num_variants, int) or num_variants < 1 or num_variants > 12:
            return jsonify({
                'error': 'num_variants must be an integer between 1 and 12'
            }), 400
        
        # Extract initials
        initials = generator.extract_initials(first_name, last_name)
        
        # Generate variants
        variants = generator.generate_variants(initials, num_variants)
        
        response = {
            'success': True,
            'user_info': {
                'first_name': first_name,
                'last_name': last_name,
                'initials': initials
            },
            'variants': variants,
            'total_variants': len(variants),
            'message': f'Generated {len(variants)} variants for {first_name} {last_name}'
        }
        
        logger.info(f"Generated {len(variants)} variants for {first_name} {last_name}")
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error generating variants: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/image/<initials>/<filename>', methods=['GET'])
def serve_image(initials, filename):
    """Serve generated profile images"""
    try:
        filepath = os.path.join(OUTPUT_DIR, initials, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'Image not found'}), 404
        
        return send_file(filepath, mimetype='image/png')
        
    except Exception as e:
        logger.error(f"Error serving image: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/image-base64/<initials>/<filename>', methods=['GET'])
def serve_image_base64(initials, filename):
    """Serve image as base64 encoded string"""
    try:
        filepath = os.path.join(OUTPUT_DIR, initials, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'Image not found'}), 404
        
        with open(filepath, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'initials': initials,
            'filename': filename,
            'image_base64': f"data:image/png;base64,{encoded_string}"
        })
        
    except Exception as e:
        logger.error(f"Error serving base64 image: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/bulk-generate', methods=['POST'])
def bulk_generate():
    """Generate profile images for multiple users"""
    try:
        data = request.get_json()
        
        if not data or 'users' not in data:
            return jsonify({'error': 'Users array is required'}), 400
        
        users = data['users']
        if not isinstance(users, list):
            return jsonify({'error': 'Users must be an array'}), 400
        
        results = []
        
        for user in users:
            try:
                first_name = user.get('first_name', '').strip()
                last_name = user.get('last_name', '').strip()
                
                if not first_name or not last_name:
                    results.append({
                        'user': user,
                        'success': False,
                        'error': 'Both first_name and last_name are required'
                    })
                    continue
                
                initials = generator.extract_initials(first_name, last_name)
                variant = generator.get_random_variant(initials)
                
                results.append({
                    'user': user,
                    'success': True,
                    'initials': initials,
                    'image': variant
                })
                
            except Exception as e:
                results.append({
                    'user': user,
                    'success': False,
                    'error': str(e)
                })
        
        successful = len([r for r in results if r['success']])
        
        return jsonify({
            'success': True,
            'total_users': len(users),
            'successful_generations': successful,
            'failed_generations': len(users) - successful,
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Error in bulk generation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/colors', methods=['GET'])
def get_colors():
    """Get available background colors"""
    return jsonify({
        'success': True,
        'colors': BACKGROUND_COLORS,
        'total_colors': len(BACKGROUND_COLORS),
        'description': 'Spiritual and cultural color palette for MyTempleYatra'
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get generation statistics"""
    try:
        stats = {
            'total_initials': 0,
            'total_variants': 0,
            'initials_generated': []
        }
        
        if os.path.exists(OUTPUT_DIR):
            for initials_dir in os.listdir(OUTPUT_DIR):
                initials_path = os.path.join(OUTPUT_DIR, initials_dir)
                if os.path.isdir(initials_path):
                    stats['total_initials'] += 1
                    variants = len([f for f in os.listdir(initials_path) if f.endswith('.png')])
                    stats['total_variants'] += variants
                    stats['initials_generated'].append({
                        'initials': initials_dir,
                        'variants': variants
                    })
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create initial directory structure
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("🚀 MyTempleYatra Profile Image Generator API")
    print("=" * 50)
    print("📊 Available endpoints:")
    print("  POST /generate - Generate single profile image")
    print("  POST /generate-variants - Generate multiple variants")
    print("  POST /bulk-generate - Generate for multiple users")
    print("  GET  /image/<initials>/<filename> - Serve image")
    print("  GET  /image-base64/<initials>/<filename> - Serve as base64")
    print("  GET  /colors - Get available colors")
    print("  GET  /stats - Get generation statistics")
    print("  GET  /health - Health check")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

    