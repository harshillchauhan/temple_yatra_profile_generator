## 🌟 Overview

The MyTempleYatra Profile Image Generator is an automated system designed to create personalized, initial-based profile images for new users registering on [MyTempleYatra.in](https://app.MyTempleYatra.in). This system ensures every user has a visually appealing profile image from the moment they register, eliminating empty or default avatars.

### 🎯 Key Objectives

- **Automated Profile Creation**: Generate profile images automatically during user registration
- **Personalized Initials**: Create images based on user's first and last name initials
- **Visual Variety**: Provide multiple design variants with different color schemes
- **Cultural Consistency**: Maintain MyTempleYatra's spiritual and cultural theme through color palette
- **Scalable Solution**: Support bulk generation for multiple users

## ✨ Features

### Core Features
- ✅ **Single Image Generation**: Generate one profile image per user
- ✅ **Multiple Variants**: Create up to 12 different design variants
- ✅ **Bulk Processing**: Generate images for multiple users simultaneously
- ✅ **RESTful API**: Complete REST API with comprehensive endpoints
- ✅ **Image Serving**: Direct image serving and base64 encoding
- ✅ **Statistics Tracking**: Monitor generation statistics and usage
- ✅ **Error Handling**: Robust error handling and validation

### Design Features
- 🎨 **Spiritual Color Palette**: 12 carefully selected colors reflecting Indian spiritual themes
- 🔤 **Clean Typography**: Bold, readable initials with proper centering
- 📐 **Consistent Dimensions**: Standard 400x400px images for uniform appearance
- 🎭 **Random Variety**: Automatic random variant selection for diversity

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python Flask |
| **Image Processing** | Pillow (PIL) |
| **Font System** | TrueType fonts |
| **API Format** | JSON REST API |
| **Storage** | Local file system |

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

```cmd
# Clone the repository
git clone https://github.com/mytempleyatra/profile-generator.git
cd profile-generator

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python profile_image_api.py
```

The server will be available at `http://localhost:5000`

### Quick Test

```cmd
# Test the API
curl -X POST http://localhost:5000/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"first_name\": \"John\", \"last_name\": \"Doe\"}"
```

## 📁 Project Structure

```
temple-yatra-profile-generator/
├── 📄 profile_image_api.py          # Main API server
├── 🧪 api_test_documentation.py     # Comprehensive testing script
├── 📋 requirements.txt              # Python dependencies
├── 📖 README.md                     # This documentation
├── 🐍 venv/                        # Virtual environment
└── 🖼️ generated_images/            # Generated profile images
    ├── AB/                         # Initials-based folders
    │   ├── AB_variant1.png
    │   ├── AB_variant2.png
    │   └── ...
    └── XY/
        ├── XY_variant1.png
        └── ...
```

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check |
| POST | `/generate` | Generate single profile image |
| POST | `/generate-variants` | Generate multiple variants |
| POST | `/bulk-generate` | Generate for multiple users |
| GET | `/image/<initials>/<filename>` | Serve image directly |
| GET | `/image-base64/<initials>/<filename>` | Serve image as base64 |
| GET | `/colors` | Get available color palette |
| GET | `/stats` | Get generation statistics |

### Example Usage

#### Generate Single Profile Image

```cmd
curl -X POST http://localhost:5000/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"first_name\": \"Arjun\", \"last_name\": \"Sharma\"}"
```

**Response:**
```json
{
  "success": true,
  "user_info": {
    "first_name": "Arjun",
    "last_name": "Sharma",
    "initials": "AS"
  },
  "image": {
    "variant": 1,
    "filename": "AS_variant1.png",
    "filepath": "generated_images/AS/AS_variant1.png",
    "bg_color": "#FF9933",
    "url": "/image/AS/AS_variant1.png"
  },
  "message": "Profile image generated successfully for Arjun Sharma"
}
```

#### Generate Multiple Variants

```cmd
curl -X POST http://localhost:5000/generate-variants ^
  -H "Content-Type: application/json" ^
  -d "{\"first_name\": \"Priya\", \"last_name\": \"Patel\", \"num_variants\": 5}"
```

#### Bulk Generation

```cmd
curl -X POST http://localhost:5000/bulk-generate ^
  -H "Content-Type: application/json" ^
  -d "{\"users\": [{\"first_name\": \"Ganesh\", \"last_name\": \"Iyer\"}, {\"first_name\": \"Lakshmi\", \"last_name\": \"Devi\"}, {\"first_name\": \"Karthik\", \"last_name\": \"Reddy\"}]}"
```

## 🎨 Color Palette

Our spiritual color palette reflects Indian cultural themes:

| Color | Hex Code | Significance |
|-------|----------|-------------|
| 🟧 Saffron | `#FF9933` | Sacred Hindu color |
| 🟨 Gold | `#FFD700` | Divine and auspicious |
| 🟣 Purple | `#A569BD` | Spirituality and wisdom |
| 🟢 Turquoise | `#1ABC9C` | Tranquility and peace |
| 🔵 Dark Blue | `#2C3E50` | Depth and devotion |
| 🔴 Red | `#E74C3C` | Energy and power |
| 🟠 Orange | `#F39C12` | Warmth and enthusiasm |
| 🟢 Green | `#27AE60` | Growth and harmony |
| 🟣 Deep Purple | `#8E44AD` | Mysticism |
| 🟠 Dark Orange | `#D35400` | Vitality |
| 🔵 Blue | `#2980B9` | Trust and stability |
| 🔴 Dark Red | `#C0392B` | Passion and strength |

## 🧪 Testing

### Automated Testing
```bash
python api_test_documentation.py
```

### Manual Testing
```cmd
# Health check
curl http://localhost:5000/health

# Get available colors
curl http://localhost:5000/colors

# Get statistics
curl http://localhost:5000/stats
```

## 🔧 Configuration

### Font Configuration

The system automatically detects and uses system fonts:

- **Windows**: Arial (`C:\Windows\Fonts\arial.ttf`)
- **Linux**: DejaVu Sans Bold (`/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`)
- **macOS**: Arial (`/System/Library/Fonts/Arial.ttf`)

### Production Settings

```python
# Add to profile_image_api.py
import os
from flask import Flask

app = Flask(__name__)

# Production settings
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    OUTPUT_DIR = os.environ.get('IMAGE_STORAGE_PATH', 'C:\\inetpub\\wwwroot\\temple-yatra\\images')
```

## 🔮 Future Enhancements

### Planned Features

- [ ] **Advanced Customization**: Multiple font options, custom color palettes
- [ ] **Template-based Designs**: Different layout templates
- [ ] **AI-powered Suggestions**: Smart design recommendations

### Technical Improvements

- [ ] **Performance**: Caching mechanisms, async processing
- [ ] **Scalability**: Microservices architecture, load balancing
- [ ] **Reliability**: Health monitoring, automatic failover

## 🤝 Integration Example

### Registration Flow Integration

```python
@app.route('/register', methods=['POST'])
def register_user():
    user_data = request.get_json()
    
    # Generate profile image
    profile_response = requests.post(
        'http://profile-generator:5000/generate',
        json={
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name']
        }
    )
    
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        user_data['profile_image_url'] = profile_data['image']['url']
    
    return create_user(user_data)
```

## 📈 Performance Metrics

| Metric | Expected Value |
|--------|----------------|
| **Generation Time** | < 500ms per image |
| **Concurrent Users** | 100+ simultaneous requests |
| **Storage** | ~50KB per image |
| **Memory Usage** | ~200MB base + 50MB per request |

## 🐛 Troubleshooting

### Common Issues

**Font Loading Error**
```
Could not load custom font, using default
```
**Solution**: Install required fonts or update font paths

**Permission Denied**
```
Permission denied: generated_images/
```
**Solution**: Check directory permissions
```cmd
# Windows - Grant full control to the folder
icacls generated_images /grant Everyone:(F)

# Or create the directory if it doesn't exist
mkdir generated_images
```

**JSON Parsing Error**
```
Invalid JSON format
```
**Solution**: Ensure proper Content-Type header and valid JSON

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

