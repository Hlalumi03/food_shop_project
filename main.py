from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import create_tables
from app.routes import api_router
import os

# Create tables on startup
create_tables()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="A professional food shop API with clean architecture"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", response_class=HTMLResponse)
def read_root():
    """Root endpoint - serves the frontend."""
    try:
        with open(os.path.join(os.path.dirname(__file__), "index.html"), "r") as f:
            return f.read()
    except FileNotFoundError:
        return {
            "message": "Welcome to Food Shop API",
            "version": settings.PROJECT_VERSION,
            "docs": f"{settings.API_V1_STR}/docs",
            "frontend": "Frontend not found. Please ensure index.html is in the root directory."
        }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/qr/foods/qr/display", response_class=HTMLResponse)
def qr_foods_display():
    """Display foods with QR code generation links."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Food Shop - QR Code Generator</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            header {
                color: white;
                margin-bottom: 40px;
                text-align: center;
            }
            header h1 {
                font-size: 36px;
                margin-bottom: 10px;
            }
            header p {
                font-size: 16px;
                opacity: 0.9;
            }
            .welcome-box {
                background: white;
                border-radius: 10px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            }
            .welcome-box h2 {
                color: #667eea;
                margin-bottom: 15px;
            }
            .welcome-box p {
                color: #666;
                margin-bottom: 10px;
                line-height: 1.6;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .feature {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            }
            .feature-icon {
                font-size: 30px;
                margin-bottom: 10px;
            }
            .feature h3 {
                color: #667eea;
                margin-bottom: 10px;
            }
            .feature p {
                color: #666;
                font-size: 14px;
            }
            .actions {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
            }
            .action-button {
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }
            .action-button:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
            .action-button a {
                display: inline-block;
                padding: 12px 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                transition: transform 0.2s ease;
            }
            .action-button a:hover {
                transform: scale(1.05);
            }
            .action-button h3 {
                color: #333;
                margin-bottom: 10px;
            }
            .action-button p {
                color: #666;
                font-size: 13px;
                margin-bottom: 15px;
            }
            .food-list {
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            }
            .food-list h2 {
                color: #667eea;
                margin-bottom: 20px;
            }
            .food-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 20px;
            }
            .food-card {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
                transition: all 0.3s ease;
            }
            .food-card:hover {
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
                border-color: #667eea;
            }
            .food-name {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            .food-info {
                color: #666;
                font-size: 13px;
                margin-bottom: 15px;
            }
            .food-info p {
                margin: 5px 0;
            }
            .food-buttons {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            .btn {
                flex: 1;
                padding: 8px 12px;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                font-size: 12px;
                text-align: center;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            .btn-qr {
                background: #667eea;
                color: white;
            }
            .btn-qr:hover {
                background: #764ba2;
            }
            .btn-api {
                background: #f0f0f0;
                color: #333;
            }
            .btn-api:hover {
                background: #e0e0e0;
            }
            .loading {
                text-align: center;
                padding: 40px;
                color: white;
            }
            .error {
                background: #f8d7da;
                color: #842029;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Food Shop QR Code Generator</h1>
                <p>Generate and scan QR codes for foods, orders, and payments</p>
            </header>
            
            <div class="welcome-box">
                <h2>Welcome to QR Code Management</h2>
                <p><strong>Scan to Pay & View:</strong> Generate QR codes that customers can scan to view food details, track orders, and make payments.</p>
                <p><strong>Multiple Options:</strong> Create QR codes for individual foods, orders, or payments.</p>
                <p><strong>Easy Integration:</strong> Each food item, order, and payment has its own dedicated QR page.</p>
            </div>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">📱</div>
                    <h3>Scan to View Foods</h3>
                    <p>Generate QR codes for food items. Customers can scan to view details and add to cart.</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">💳</div>
                    <h3>Scan to Pay</h3>
                    <p>Create QR codes for payments. Customers can scan to complete transactions instantly.</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">📦</div>
                    <h3>Track Orders</h3>
                    <p>Generate QR codes for orders. Customers can scan to track order status in real-time.</p>
                </div>
            </div>
            
            <div class="actions">
                <div class="action-button">
                    <h3>Foods</h3>
                    <p>View and generate QR codes for all food items</p>
                    <a href="#foods-section">View Foods</a>
                </div>
                <div class="action-button">
                    <h3>API Documentation</h3>
                    <p>Explore all available API endpoints</p>
                    <a href="/api/v1/docs">API Docs</a>
                </div>
                <div class="action-button">
                    <h3>Direct QR Endpoints</h3>
                    <p>Access QR code endpoints directly</p>
                    <a href="#endpoints">View Endpoints</a>
                </div>
            </div>
            
            <div style="margin-top: 40px; color: white; font-size: 14px;">
                <h3>QR Code Endpoints</h3>
                <ul style="margin-top: 10px; margin-left: 20px;">
                    <li><code>/api/v1/qr/foods/{id}/qr</code> - Get QR code image for a food</li>
                    <li><code>/api/v1/qr/foods/{id}/qr/page</code> - Get QR page for a food</li>
                    <li><code>/api/v1/qr/orders/{id}/qr</code> - Get QR code image for an order</li>
                    <li><code>/api/v1/qr/orders/{id}/qr/page</code> - Get QR page for an order</li>
                    <li><code>/api/v1/qr/payments/{id}/qr</code> - Get QR code image for a payment</li>
                    <li><code>/api/v1/qr/payments/{id}/qr/page</code> - Get QR page for a payment (Scan to Pay)</li>
                </ul>
            </div>
            
            <div class="food-list" id="foods-section" style="margin-top: 40px;">
                <h2>Available Foods</h2>
                <div class="food-grid" id="foodGrid">
                    <div class="loading">
                        <p>Loading foods...</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            async function loadFoods() {
                try {
                    const response = await fetch('/api/v1/foods');
                    const foods = await response.json();
                    const foodGrid = document.getElementById('foodGrid');
                    
                    if (!Array.isArray(foods) || foods.length === 0) {
                        foodGrid.innerHTML = '<div class="error">No foods available. Create some foods first via the API!</div>';
                        return;
                    }
                    
                    foodGrid.innerHTML = '';
                    foods.forEach(food => {
                        const card = document.createElement('div');
                        card.className = 'food-card';
                        card.innerHTML = `
                            <div class="food-name">${food.name}</div>
                            <div class="food-info">
                                <p><strong>Price:</strong> $${food.price.toFixed(2)}</p>
                                <p><strong>Category:</strong> ${food.category}</p>
                                <p><strong>Stock:</strong> ${food.stock}</p>
                            </div>
                            <div class="food-buttons">
                                <a href="/api/v1/qr/foods/${food.id}/qr/page" class="btn btn-qr">🔲 QR Code</a>
                                <a href="/api/v1/foods/${food.id}" class="btn btn-api">📄 Details</a>
                            </div>
                        `;
                        foodGrid.appendChild(card);
                    });
                } catch (error) {
                    document.getElementById('foodGrid').innerHTML = '<div class="error">Error loading foods: ' + error.message + '</div>';
                }
            }
            
            loadFoods();
        </script>
    </body>
    </html>
    """
    return html


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
