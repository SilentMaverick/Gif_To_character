# 🎨 ASCII Art Converter - Web Application

A modern, responsive web application that converts GIF images to ASCII art with a beautiful user interface, Gmail authentication, token reward system, and **advanced face animation capabilities**.

## ✨ Features

### 🚀 Core Functionality
- **GIF to ASCII Conversion**: Convert animated GIFs to stunning ASCII art
- **Multiple Output Formats**: GIF or plain text output
- **Customizable Settings**: Scale, speed, colors, font size, brightness inversion
- **Real-time Preview**: See your file before conversion
- **Drag & Drop Upload**: Modern file upload interface

### 🎭 **Face Animation System** ✨
- **Automatic Face Detection**: Advanced facial landmark detection using dlib
- **Live Facial Expressions**: Make faces blink, smile, and move eyebrows
- **Real-time Animation**: Frame-by-frame face tracking and animation
- **Preview Feature**: See face animations before converting
- **Multiple Face Support**: Handle GIFs with multiple faces
- **Customizable Timing**: Adjustable animation intervals and durations

### 🔐 Authentication & User Management
- **Gmail OAuth Integration**: Secure sign-in with Google accounts
- **Token Reward System**: Earn tokens for conversions and Gmail users
- **User Dashboard**: Track conversions and manage profile
- **Session Management**: Secure user sessions

### 🎨 Modern UI/UX
- **Responsive Design**: Works perfectly on all devices
- **Smooth Animations**: Beautiful transitions and hover effects
- **Material Design**: Clean, modern interface
- **Dark/Light Themes**: Beautiful gradient backgrounds

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: User session management
- **Pillow**: Image processing
- **NumPy**: Numerical operations

### 🎭 **Face Animation Engine**
- **OpenCV**: Computer vision and image processing
- **dlib**: Advanced facial landmark detection
- **Facial Landmarks**: 68-point face mapping system
- **Real-time Processing**: Frame-by-frame animation generation

### Frontend
- **HTML5/CSS3**: Modern markup and styling
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Beautiful icons
- **Google Fonts**: Typography
- **CSS Grid/Flexbox**: Responsive layouts

### Database
- **SQLite**: Lightweight database (can be upgraded to PostgreSQL/MySQL)

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ascii-art-converter
   ```

2. **Install core dependencies**
   ```bash
   pip install -r web_requirements.txt
   ```

3. **Install face animation dependencies** (optional but recommended)
   ```bash
   pip install -r face_requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
ascii-art-converter/
├── app.py                 # Main Flask application
├── new.py                # Core conversion logic
├── face_animator.py      # 🎭 Face animation engine
├── demo_face_animation.py # Face animation demo script
├── templates/            # HTML templates
│   ├── index.html        # Landing page
│   ├── converter.html    # Main converter interface
│   ├── dashboard.html    # User dashboard
│   └── login.html        # Authentication page
├── uploads/              # File upload directory
├── web_requirements.txt  # Web app dependencies
├── face_requirements.txt # 🎭 Face animation dependencies
├── requirements.txt      # Core converter dependencies
└── README.md            # Core converter documentation
```

## 🎭 **Face Animation Features**

### **What It Does**
- **Detects faces** in GIF frames automatically
- **Tracks facial landmarks** (eyes, nose, mouth, eyebrows)
- **Adds animations** like blinking, smiling, eyebrow movement
- **Creates previews** so you can see the effect before converting
- **Overlays ASCII faces** on the original images

### **Animation Types**
1. **👁️ Eye Animations**
   - Blinking (every 30-60 frames)
   - Half-closed eyes
   - Smooth transitions

2. **😊 Mouth Expressions**
   - Smiling (every 80-120 frames)
   - Slight smiles
   - Happy expressions

3. **🤨 Eyebrow Movements**
   - Raised eyebrows (every 60-90 frames)
   - Subtle movements
   - Expression enhancement

### **How to Use Face Animation**
1. **Upload a GIF** with faces
2. **Click "Preview"** to see face animations
3. **Enable "Face Animation"** checkbox
4. **Convert** (costs 2 tokens instead of 1)
5. **Download** your animated ASCII art!

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set custom secret key
export FLASK_SECRET_KEY="your-secret-key"

# Optional: Set custom database URI
export DATABASE_URL="sqlite:///ascii_converter.db"
```

### Face Animation Settings
```python
# In face_animator.py, you can customize:
BLINK_INTERVAL = 45      # Frames between blinks
SMILE_INTERVAL = 100     # Frames between smiles
EYEBROW_INTERVAL = 75    # Frames between eyebrow movements
```

## 🎯 Usage Guide

### 1. Landing Page (`/`)
- Beautiful hero section with feature highlights
- Token system explanation
- **Face animation feature showcase**
- Call-to-action buttons

### 2. Authentication (`/login`)
- Gmail OAuth integration
- Demo login option
- Benefits explanation

### 3. Converter (`/converter`)
- Drag & drop file upload
- **Face animation controls and preview**
- Customizable conversion settings
- Real-time progress tracking
- Download results

### 4. Dashboard (`/dashboard`)
- User profile information
- Conversion history
- Token balance
- Usage statistics

## 🔐 Authentication Flow

### Gmail OAuth (Production)
1. User clicks "Sign in with Gmail"
2. Redirected to Google OAuth
3. User authorizes application
4. Google returns authorization code
5. Application exchanges code for access token
6. User profile created/updated
7. User redirected to dashboard

### Demo Login (Development)
1. User clicks "Demo Login"
2. Mock user session created
3. User redirected to dashboard
4. Full functionality available

## 🪙 Token System

### Token Allocation
- **New Users**: 100 tokens
- **Gmail Users**: +50 bonus tokens
- **Basic Conversion**: -1 token
- **🎭 Face Animation**: -2 tokens (premium feature)
- **Rewards**: Earn tokens through usage

### Token Benefits
- Convert GIFs to ASCII art
- **Access face animation features**
- Access premium features
- Priority processing
- Extended file size limits

## 🎨 Customization

### Styling
- Modify CSS in template files
- Update color schemes in `:root` variables
- Customize animations and transitions

### Features
- Add new conversion options
- Implement additional output formats
- **Extend face animation system**
- Extend token reward system
- Add social sharing features

### Face Animation Customization
```python
# Customize animation timing
def calculate_blink_factor(self, frame_index, total_frames):
    blink_interval = 30  # More frequent blinking
    blink_duration = 2   # Faster blinks
    
# Add new expressions
def calculate_wink_factor(self, frame_index, total_frames):
    # Custom wink animation
    pass
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Using Docker
docker build -t ascii-converter .
docker run -p 8000:8000 ascii-converter
```

### Environment Setup
1. Set `FLASK_ENV=production`
2. Configure production database
3. Set secure secret key
4. Enable HTTPS
5. Configure reverse proxy (Nginx)

## 🔒 Security Features

- **CSRF Protection**: Built-in Flask security
- **Secure File Uploads**: File type validation
- **Session Management**: Secure user sessions
- **Input Validation**: Sanitized user inputs
- **Rate Limiting**: API request throttling

## 📱 Mobile Responsiveness

- **Responsive Grid**: CSS Grid and Flexbox
- **Mobile-First**: Optimized for small screens
- **Touch-Friendly**: Large touch targets
- **Progressive Web App**: Installable on mobile

## 🧪 Testing

### Manual Testing
1. Test file upload functionality
2. Verify conversion process
3. **Test face animation features**
4. Check authentication flow
5. Test responsive design
6. Validate token system

### Face Animation Testing
```bash
# Run the demo script
python demo_face_animation.py

# Test with sample GIFs
python face_animator.py
```

### Automated Testing
```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility

2. **Face Animation Issues**
   - Install OpenCV: `pip install opencv-python`
   - Install dlib: `pip install dlib`
   - Check facial landmark predictor file

3. **Database Issues**
   - Verify database file permissions
   - Check SQLite installation

4. **File Upload Problems**
   - Check upload directory permissions
   - Verify file size limits

5. **Authentication Issues**
   - Check OAuth configuration
   - Verify session settings

## 🎭 **Face Animation Tips**

### **Best Practices**
- Use GIFs with clear, front-facing faces
- Higher resolution GIFs work better
- Multiple frames show more animation variety
- Good lighting improves face detection

### **Troubleshooting Face Animation**
- **No faces detected**: Check image quality and face orientation
- **Poor animation**: Ensure GIF has enough frames
- **Slow processing**: Reduce GIF size or frame count
- **Missing landmarks**: Install dlib and facial predictor

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

### **Face Animation Contributions**
- Add new facial expressions
- Improve detection accuracy
- Optimize animation performance
- Add emotion recognition

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Pillow developers for image processing capabilities
- **OpenCV and dlib teams** for computer vision capabilities
- Font Awesome for beautiful icons
- Google Fonts for typography

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review troubleshooting section
- **Test face animation with demo script**

---

**Made with ❤️ using modern web technologies and AI-powered face animation** 🎭✨ 