"""
Quick Start Script for ED Demand Forecasting Dashboard
"""
import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'pandas', 'numpy', 'plotly', 'sklearn']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed!")
    return True

def main():
    print("=" * 60)
    print("🏥 Emergency Department Demand Forecasting Dashboard")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if app.py exists
    app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    if not os.path.exists(app_path):
        print(f"❌ Error: app.py not found at {app_path}")
        sys.exit(1)
    
    print("\n🚀 Starting Streamlit dashboard...")
    print("📊 Dashboard will open in your browser automatically")
    print("🌐 Running on port 9548")
    print("💡 Press Ctrl+C to stop the server\n")
    
    try:
        # Run streamlit on port 9548
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', app_path, '--server.port', '9548'])
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped.")
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

