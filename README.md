# 🪵 Professional 3D Wooden Cutting Plan Optimizer

A production-ready, full-stack web application to optimize wooden cutting plans for packaging manufacturing—focused on maximizing material utilization, minimizing waste, and producing clear output/diagrams for saw operators.

## 🎯 Features

### Core Functionality
- **Inventory Management**: Enter available lumber/board stock with dimensions, quantity, and cost
- **Parts Definition**: Define required cut-parts with dimensions, quantities, and material requirements
- **Advanced Parameters**: Configure kerf, tolerances, grain direction enforcement, and optimization priorities
- **3D Guillotine Algorithm**: Advanced cutting optimization with material nesting and offcut tracking
- **Interactive Visualization**: 2D and 3D SVG visualizations of cutting plans
- **Export Capabilities**: PDF reports and CSV data export

### User Experience
- **Modern UI**: Clean, responsive interface with dark/light mode support
- **Step-by-Step Workflow**: Guided process from input to results
- **Real-time Validation**: Input validation and error handling
- **Sample Data**: Pre-loaded pallet packaging example for testing

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation & Running

1. **Clone and navigate to the project**
   ```bash
   cd /workspace
   ```

2. **Start the application**
   ```bash
   ./start.sh
   ```

   This will:
   - Install Python dependencies (FastAPI, optimization libraries)
   - Install Node.js dependencies (React, visualization libraries)
   - Start the FastAPI backend on port 8000
   - Start the React frontend on port 3000

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup (Alternative)

If you prefer to run the services separately:

**Backend (FastAPI)**
```bash
cd backend
pip install -r ../requirements.txt
python main.py
```

**Frontend (React)**
```bash
npm install
npm start
```

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **FastAPI** for high-performance API
- **Advanced 3D Guillotine Algorithm** for cutting optimization
- **Material nesting** with offcut tracking and reuse
- **RESTful API** with comprehensive error handling

### Frontend (React/TypeScript)
- **React 18** with TypeScript for type safety
- **Modern UI Components** with responsive design
- **SVG Visualization** for cutting plans and layouts
- **Export Functionality** for PDF reports and CSV data

### Key Algorithms
- **3D Guillotine Cutting**: Optimizes material usage across length, width, and thickness
- **Rotation Handling**: Supports part rotation with grain direction constraints
- **Offcut Management**: Tracks and reuses leftover materials
- **Tolerance Processing**: Handles dimensional tolerances for practical manufacturing

## 📊 Sample Data

The application includes sample data for pallet packaging:
- **Lumber Stock**: Aus KD Pine 8'×7"×3.5" and Standard 2×4×8'
- **Parts**: Pallet deck boards, stringers, and corner blocks
- **Parameters**: Industry-standard cutting parameters

## 🎨 User Interface

### Step 1: Inventory
- Add lumber stock with dimensions and quantities
- Real-time validation and cost tracking
- Bulk import capabilities

### Step 2: Parts
- Define cut parts with detailed specifications
- Priority-based optimization
- Material type and rotation constraints

### Step 3: Parameters
- Configure cutting parameters (kerf, tolerance, etc.)
- Optimization priority selection
- Grain direction enforcement

### Step 4: Optimization
- Review inputs and run optimization
- Real-time progress indication
- Error handling and validation

### Step 5: Results
- Comprehensive results dashboard
- Interactive cutting plan visualizations
- Export capabilities (PDF/CSV)

## 🔧 API Endpoints

- `GET /` - API status
- `POST /optimize` - Run cutting optimization
- `GET /sample-data` - Get sample data for testing

## 📈 Optimization Metrics

- **Material Utilization**: Percentage of lumber used effectively
- **Waste Reduction**: Minimize leftover materials
- **Cut Efficiency**: Optimize number of cuts required
- **Cost Optimization**: Minimize material costs

## 🎯 Target Users

- **Industrial Designers**: Optimize packaging designs
- **Manufacturing Managers**: Improve material efficiency
- **Shop Floor Operators**: Clear cutting instructions
- **Packaging Engineers**: Professional optimization tools

## 🛠️ Development

### Project Structure
```
/workspace/
├── backend/           # FastAPI backend
│   ├── main.py       # API server
│   └── optimization_algorithm.py  # Core algorithm
├── src/              # React frontend
│   ├── components/   # UI components
│   ├── contexts/     # React contexts
│   ├── types/        # TypeScript types
│   └── utils/        # Utility functions
├── public/           # Static assets
└── requirements.txt  # Python dependencies
```

### Key Technologies
- **Backend**: FastAPI, NumPy, SciPy, Pydantic
- **Frontend**: React, TypeScript, Lucide React, jsPDF
- **Visualization**: SVG, Canvas API
- **Styling**: CSS Custom Properties, Responsive Design

## 📝 License

This project is developed for Greenstrand Packaging and is proprietary software.

## 🤝 Contributing

This is a professional application developed for specific industrial requirements. For modifications or enhancements, please contact the development team.

---

**Built with ❤️ for Greenstrand Packaging - Optimizing Wood Cutting Since 2024**
