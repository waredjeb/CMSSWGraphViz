# Installation Guide

Complete installation instructions for CMSSW Graph Visualization on different platforms.

## Quick Install (All Platforms)

If you already have Python 3.6+ and graphviz installed:

```bash
cd CMSSWGraph
chmod +x run.sh
./run.sh
```

That's it! Open http://localhost:8000/app/

---

## Platform-Specific Instructions

### Ubuntu / Debian

**1. Install system dependencies:**

```bash
# Update package list
sudo apt update

# Install Python 3, pip, venv, and graphviz
sudo apt install python3 python3-pip python3-venv graphviz
```

**2. Verify installation:**

```bash
python3 --version   # Should be 3.6 or higher
pip3 --version      # Should show pip version
dot -V              # Should show graphviz version
```

**3. Run the application:**

```bash
cd CMSSWGraph
chmod +x run.sh
./run.sh
```

**4. Open browser:**

Navigate to: http://localhost:8000/app/

---

### CentOS / RHEL / Fedora

**1. Install system dependencies:**

```bash
# CentOS/RHEL 7
sudo yum install python3 python3-pip graphviz

# CentOS/RHEL 8+ or Fedora
sudo dnf install python3 python3-pip graphviz
```

**2. Verify installation:**

```bash
python3 --version
pip3 --version
dot -V
```

**3. Run the application:**

```bash
cd CMSSWGraph
chmod +x run.sh
./run.sh
```

---

### macOS

**1. Install Homebrew** (if not already installed):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2. Install dependencies:**

```bash
# Install Python 3 and graphviz
brew install python3 graphviz
```

**3. Verify installation:**

```bash
python3 --version
pip3 --version
dot -V
```

**4. Run the application:**

```bash
cd CMSSWGraph
chmod +x run.sh
./run.sh
```

---

### Windows (WSL2)

**Recommended:** Use Windows Subsystem for Linux 2 (WSL2) with Ubuntu.

**1. Enable WSL2:**

Open PowerShell as Administrator and run:

```powershell
wsl --install
```

**2. Install Ubuntu from Microsoft Store**

**3. Open Ubuntu terminal and follow Ubuntu instructions:**

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv graphviz
cd /mnt/c/path/to/CMSSWGraph
chmod +x run.sh
./run.sh
```

**4. Open browser on Windows:**

Navigate to: http://localhost:8000/app/

---

### Windows (Native Python)

**Not recommended** due to graphviz complexity. Use WSL2 instead.

If you must use native Windows:

**1. Install Python 3.6+:**
- Download from: https://www.python.org/downloads/
- Check "Add Python to PATH" during installation

**2. Install graphviz:**
- Download from: https://graphviz.org/download/
- Add graphviz bin directory to PATH

**3. Run manually:**

```cmd
cd CMSSWGraph
python -m venv venv
venv\Scripts\activate
pip install -r preprocess\requirements.txt
python preprocess\build_bundle.py
python server.py
```

---

## Troubleshooting Installation

### Python Version Too Old

**Error:** `Python 3.5 or lower detected`

**Solution:**

```bash
# Ubuntu/Debian - install newer Python
sudo apt install python3.8 python3.8-venv python3-pip

# Update run.sh to use python3.8 instead of python3
```

### graphviz Not Found

**Error:** `ImportError: failed to execute PosixPath('dot')`

**Solution:**

```bash
# Ubuntu/Debian
sudo apt install graphviz

# CentOS/RHEL
sudo yum install graphviz

# macOS
brew install graphviz

# Verify installation
dot -V
```

### pip Not Found

**Error:** `pip: command not found`

**Solution:**

```bash
# Ubuntu/Debian
sudo apt install python3-pip

# Or use python3 -m pip instead
python3 -m pip install -r preprocess/requirements.txt
```

### Virtual Environment Creation Fails

**Error:** `The virtual environment was not created successfully`

**Solution:**

```bash
# Install venv module
sudo apt install python3-venv  # Ubuntu/Debian
sudo yum install python3-venv  # CentOS/RHEL
```

### Permission Denied on run.sh

**Error:** `bash: ./run.sh: Permission denied`

**Solution:**

```bash
chmod +x run.sh
```

### Port 8000 Already in Use

**Error:** `OSError: [Errno 98] Address already in use`

**Solution:**

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or edit server.py to use a different port
```

---

## Verifying Installation

After running `./run.sh`, you should see:

```
============================================================
CMSSW Module Dependency Graph Visualization
============================================================

Serving from: /path/to/CMSSWGraph
Server address: http://localhost:8000
Application URL: http://localhost:8000/app/

Press Ctrl+C to stop the server
============================================================
```

**Test the application:**

1. Open browser to http://localhost:8000/app/
2. You should see the graph visualization
3. Click any node to verify the side panel opens
4. Try searching for a module
5. Test keyboard navigation (arrow keys)

If all these work, installation is successful! ✅

---

## Uninstallation

To remove the application:

```bash
# Stop the server (Ctrl+C)

# Remove virtual environment
rm -rf venv/

# Remove generated bundle (optional)
rm -f data/bundle.json

# The application files remain for future use
# To completely remove:
cd ..
rm -rf CMSSWGraph/
```

---

## Updating

To update the application:

```bash
# Pull latest changes (if using git)
git pull

# Remove old virtual environment
rm -rf venv/

# Regenerate bundle (if input files changed)
rm -f data/bundle.json

# Run again
./run.sh
```

---

## System Requirements

**Minimum:**
- CPU: 1 core
- RAM: 2 GB
- Disk: 500 MB (for application + bundle)
- Browser: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

**Recommended:**
- CPU: 2+ cores
- RAM: 4 GB
- Disk: 1 GB
- Browser: Latest version of Chrome or Firefox

**Network:**
- No internet required (runs locally)
- Uses localhost (127.0.0.1) only

---

## Docker Installation (Alternative)

**Coming soon:** Docker image for easier deployment.

For now, use the native installation methods above.

---

## Getting Help

If you encounter issues not covered here:

1. Check the [Troubleshooting](#troubleshooting-installation) section above
2. Check the main [README.md](README.md) Troubleshooting section
3. Verify all prerequisites are installed correctly
4. Check browser console for JavaScript errors
5. Check terminal for Python errors

**Common issues:**
- Missing graphviz: Install system package
- Python too old: Upgrade to 3.6+
- Port in use: Change port in server.py
- Bundle generation fails: Check input file paths

---

**For usage instructions, see [README.md](README.md)**

**For feature details, see [FEATURES.md](FEATURES.md)**
