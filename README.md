# 🪵 Professional 3D Wooden Cutting Plan Optimizer

A production-ready, full-stack web application for optimizing wooden cutting plans for packaging manufacturing. Maximizes material utilization, minimizes waste, and produces clear cutting diagrams for saw operators.

## 🎯 Features

### Core Functionality
- **Advanced 3D Guillotine Cutting Algorithm** - Optimizes material usage with rotation, nesting, and offcut tracking
- **Interactive Input Forms** - Easy data entry for lumber stock, parts lists, and cutting parameters
- **Real-time Visualization** - 2D/3D cutting plan diagrams with color-coded parts and kerf lines
- **Professional Export** - PDF reports, CSV data exports, and printable cutting plans
- **Material Efficiency Tracking** - Comprehensive utilization metrics and waste analysis

### User Experience
- **Modern UI/UX** - Clean, responsive design with dark/light mode support
- **Progressive Workflow** - Step-by-step guided process from input to results
- **Sample Data** - Pre-loaded pallet packaging examples for testing
- **Real-time Validation** - Input validation and error handling
- **Mobile Responsive** - Works on desktop, tablet, and mobile devices

## 🏗️ Architecture

### Frontend (React/Next.js)
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with custom wood-themed color palette
- **State Management**: React hooks and context
- **Visualization**: Custom SVG-based cutting plan renderer
- **Export**: jsPDF for PDF generation, native CSV download

### Backend (Python/FastAPI)
- **API**: FastAPI with automatic OpenAPI documentation
- **Algorithm**: Custom 3D guillotine cutting optimization
- **Data Models**: Pydantic for type-safe data validation
- **CORS**: Configured for frontend integration

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- pip

### Installation & Setup

1. **Clone and navigate to the project**
   ```bash
   cd /workspace
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

**Option 1: Use the startup scripts**
```bash
# Terminal 1 - Start backend
./start_backend.sh

# Terminal 2 - Start frontend
./start_frontend.sh
```

**Option 2: Manual startup**
```bash
# Terminal 1 - Start backend
cd backend
python main.py

# Terminal 2 - Start frontend
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Usage Guide

### 1. Input Data
- **Lumber Stock**: Add available lumber with dimensions and quantities
- **Parts List**: Define required cut parts with specifications
- **Load Sample Data**: Use pre-configured pallet packaging example

### 2. Cutting Parameters
- **Kerf**: Saw blade gap (default: 3mm)
- **Minimum Offcut**: Minimum reusable offcut size (default: 50mm)
- **Tolerance**: Allowable dimension deviation (default: 2mm)
- **Optimization Priority**: Efficiency, cost, or speed

### 3. Optimization
- Click "Start Optimization" to run the algorithm
- View real-time progress and results
- Analyze material utilization and waste metrics

### 4. Visualization & Export
- **2D/3D Views**: Interactive cutting plan diagrams
- **Stick Selection**: Focus on specific lumber pieces
- **Export Options**: CSV data, PDF reports, print-ready formats
- **Share Results**: Export and share optimization results

## 🔧 Technical Details

### Optimization Algorithm
The cutting optimizer implements a sophisticated 3D guillotine algorithm that:
- Considers material rotation and grain direction
- Tracks offcuts for future nesting opportunities
- Handles tolerance-based part matching
- Optimizes for efficiency, cost, or speed based on priority
- Provides detailed utilization metrics

### Data Flow
1. **Input Validation** → Frontend validates user inputs
2. **API Request** → Data sent to FastAPI backend
3. **Optimization** → Algorithm processes cutting plans
4. **Results** → Structured data returned to frontend
5. **Visualization** → SVG-based cutting diagrams rendered
6. **Export** → Multiple format options available

### Key Components
- **InputForms**: Multi-tab data entry with validation
- **OptimizationResults**: Comprehensive metrics and statistics
- **Visualization**: Interactive 2D/3D cutting plan renderer
- **ExportPanel**: Multiple export format options

## 🎨 Customization

### Theming
- Modify `tailwind.config.js` for color schemes
- Update component styles in individual files
- Customize wood-themed color palette

### Algorithm Tuning
- Adjust optimization parameters in `backend/main.py`
- Modify cutting logic in `CuttingOptimizer` class
- Add new material types and constraints

### Export Formats
- Extend CSV generation in `ExportPanel.tsx`
- Add PDF templates for professional reports
- Implement DXF export for CNC integration

## 📊 Sample Data

The application includes sample data for pallet packaging:
- **Lumber**: Aus KD Pine and Douglas Fir in standard sizes
- **Parts**: Planks, stringers, and blocks with realistic dimensions
- **Parameters**: Industry-standard cutting parameters

## 🔮 Future Enhancements

- **User Authentication**: Save and load optimization jobs
- **Offcut Database**: Track and reuse offcuts across projects
- **CNC Integration**: Direct DXF export for digital saws
- **AI Assistant**: Chat support for optimization guidance
- **Batch Comparison**: Compare multiple optimization runs
- **Advanced 3D**: Full 3D visualization with WebGL

## 🤝 Contributing

This is a professional application built for Greenstrand Packaging. For modifications or enhancements, please follow the established patterns and maintain code quality standards.

## 📄 License

Professional use license for Greenstrand Packaging optimization system.

---

**Built with ❤️ for efficient wood packaging manufacturing**
