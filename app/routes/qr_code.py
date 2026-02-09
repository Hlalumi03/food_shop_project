from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import FoodService, OrderService, PaymentService
from app.services.qr_code_service import QRCodeService
from app.schemas import PaymentCreate

router = APIRouter()


@router.get("/foods/{food_id}/qr", response_class=Response)
def get_food_qr_code(
    food_id: int,
    db: Session = Depends(get_db)
):
    """Generate QR code for a food item."""
    service = FoodService(db)
    food = service.get_food(food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    qr_code = QRCodeService.generate_food_qr_code(food_id)
    return Response(
        content=qr_code.getvalue(),
        media_type="image/png"
    )


@router.get("/foods/{food_id}/qr/page", response_class=HTMLResponse)
def get_food_qr_page(
    food_id: int,
    db: Session = Depends(get_db)
):
    """Get a page displaying the QR code for a food item."""
    service = FoodService(db)
    food = service.get_food(food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    qr_base64 = QRCodeService.generate_food_qr_code_base64(food_id)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{food.name} - QR Code</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .container {{
                background: white;
                border-radius: 10px;
                padding: 40px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                text-align: center;
                max-width: 500px;
            }}
            h1 {{
                color: #333;
                margin-bottom: 10px;
            }}
            .details {{
                background: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 30px;
                text-align: left;
            }}
            .detail-item {{
                margin: 10px 0;
            }}
            .detail-label {{
                font-weight: bold;
                color: #667eea;
            }}
            .qr-code {{
                margin: 30px 0;
                padding: 20px;
                background: #f9f9f9;
                border-radius: 5px;
            }}
            .qr-code img {{
                max-width: 300px;
                width: 100%;
                height: auto;
            }}
            .instructions {{
                color: #666;
                font-size: 14px;
                margin-top: 20px;
            }}
            .button {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                cursor: pointer;
                border: none;
                font-size: 14px;
            }}
            .button:hover {{
                background: #764ba2;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Scan to View Food</h1>
            <div class="details">
                <div class="detail-item">
                    <span class="detail-label">Food:</span> {food.name}
                </div>
                <div class="detail-item">
                    <span class="detail-label">Price:</span> ${food.price:.2f}
                </div>
                <div class="detail-item">
                    <span class="detail-label">Category:</span> {food.category}
                </div>
                <div class="detail-item">
                    <span class="detail-label">Stock:</span> {food.stock} available
                </div>
            </div>
            <div class="qr-code">
                <img src="{qr_base64}" alt="QR Code">
            </div>
            <div class="instructions">
                <p>Scan this QR code with your phone to view the food details and place an order.</p>
            </div>
            <a href="/api/v1/foods" class="button">Back to Foods</a>
        </div>
    </body>
    </html>
    """
    return html


@router.get("/orders/{order_id}/qr", response_class=Response)
def get_order_qr_code(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Generate QR code for an order."""
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    qr_code = QRCodeService.generate_order_qr_code(order_id)
    return Response(
        content=qr_code.getvalue(),
        media_type="image/png"
    )


@router.get("/orders/{order_id}/qr/page", response_class=HTMLResponse)
def get_order_qr_page(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Get a page displaying the QR code for an order."""
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    qr_base64 = QRCodeService.generate_order_qr_code_base64(order_id)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Order {order_id} - QR Code</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .container {{
                background: white;
                border-radius: 10px;
                padding: 40px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                text-align: center;
                max-width: 500px;
            }}
            h1 {{
                color: #333;
                margin-bottom: 10px;
            }}
            .details {{
                background: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 30px;
                text-align: left;
            }}
            .detail-item {{
                margin: 10px 0;
            }}
            .detail-label {{
                font-weight: bold;
                color: #667eea;
            }}
            .qr-code {{
                margin: 30px 0;
                padding: 20px;
                background: #f9f9f9;
                border-radius: 5px;
            }}
            .qr-code img {{
                max-width: 300px;
                width: 100%;
                height: auto;
            }}
            .status {{
                padding: 10px;
                border-radius: 5px;
                margin: 15px 0;
                font-weight: bold;
            }}
            .status.pending {{
                background: #fff3cd;
                color: #856404;
            }}
            .status.confirmed {{
                background: #cfe2ff;
                color: #084298;
            }}
            .status.delivered {{
                background: #d1e7dd;
                color: #0f5132;
            }}
            .instructions {{
                color: #666;
                font-size: 14px;
                margin-top: 20px;
            }}
            .button {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                cursor: pointer;
                border: none;
                font-size: 14px;
                margin-right: 10px;
            }}
            .button:hover {{
                background: #764ba2;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Order #{order_id}</h1>
            <div class="details">
                <div class="detail-item">
                    <span class="detail-label">Customer:</span> {order.customer_name}
                </div>
                <div class="detail-item">
                    <span class="detail-label">Total Amount:</span> ${order.total_amount:.2f}
                </div>
                <div class="detail-item">
                    <span class="detail-label">Payment Status:</span> {'Paid' if order.is_paid else 'Pending'}
                </div>
            </div>
            <div class="status {order.status.lower()}">
                Status: {order.status.upper()}
            </div>
            <div class="qr-code">
                <img src="{qr_base64}" alt="QR Code">
            </div>
            <div class="instructions">
                <p>Scan this QR code to view order details and track your order.</p>
            </div>
            <div style="margin-top: 30px; display: flex; gap: 10px; justify-content: center;">
                <a href="/api/v1/orders" class="button">Back to Orders</a>
                <a href="/qr/orders/{order_id}/payment/page" class="button" style="background: #28a745;">Pay Now</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html


@router.get("/orders/{order_id}/payment/page", response_class=HTMLResponse)
def get_order_payment_qr_page(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Get a page displaying payment QR for an order."""
    order_service = OrderService(db)
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get or create payment for the order
    payment_service = PaymentService(db)
    payments = payment_service.get_payments_by_order(order_id)
    
    if not payments:
        # Create a new payment for this order
        try:
            payment_create = PaymentCreate(
                order_id=order_id,
                amount=order.total_amount,
                payment_method="card"
            )
            payment = payment_service.create_payment(payment_create)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create payment: {str(e)}")
    else:
        # Use the first pending payment, or the most recent one
        payment = next((p for p in payments if p.status == "pending"), payments[-1])
    
    qr_base64 = QRCodeService.generate_payment_qr_code_base64(payment.id)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Order Payment - Scan to Pay</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
            }}
            .container {{
                background: white;
                border-radius: 15px;
                padding: 40px;
                box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
                text-align: center;
                max-width: 500px;
                width: 100%;
            }}
            h1 {{
                color: #333;
                margin-bottom: 10px;
                font-size: 28px;
            }}
            .order-info {{
                background: #f0f4ff;
                border-left: 4px solid #667eea;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
                text-align: left;
            }}
            .order-info p {{
                margin: 8px 0;
                color: #555;
            }}
            .order-info strong {{
                color: #667eea;
            }}
            .amount-box {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin: 25px 0;
            }}
            .amount-label {{
                font-size: 14px;
                opacity: 0.9;
                margin-bottom: 10px;
            }}
            .amount-value {{
                font-size: 42px;
                font-weight: bold;
            }}
            .qr-code {{
                background: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                margin: 25px 0;
                border: 2px dashed #667eea;
            }}
            .qr-code img {{
                max-width: 300px;
                width: 100%;
                height: auto;
                display: block;
                margin: 0 auto;
            }}
            .qr-label {{
                color: #666;
                font-size: 13px;
                margin-top: 10px;
                font-weight: 500;
            }}
            .payment-id {{
                background: #f5f5f5;
                padding: 12px;
                border-radius: 5px;
                margin: 15px 0;
                font-size: 13px;
                color: #888;
            }}
            .payment-id strong {{
                color: #333;
            }}
            .instructions {{
                background: #e3f2fd;
                border-left: 4px solid #2196F3;
                color: #1565c0;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
                font-size: 14px;
            }}
            .button-group {{
                display: flex;
                gap: 10px;
                margin-top: 25px;
                justify-content: center;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                cursor: pointer;
                border: none;
                font-size: 14px;
                font-weight: 600;
                transition: background 0.3s;
            }}
            .button:hover {{
                background: #764ba2;
            }}
            .button.secondary {{
                background: #6c757d;
            }}
            .button.secondary:hover {{
                background: #5a6268;
            }}
            .status-badge {{
                display: inline-block;
                background: #fff3cd;
                color: #856404;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                margin-top: 10px;
            }}
            .status-badge.paid {{
                background: #d1e7dd;
                color: #0f5132;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💳 Payment Required</h1>
            
            <div class="order-info">
                <p><strong>Order ID:</strong> #{order_id}</p>
                <p><strong>Customer:</strong> {order.customer_name}</p>
                <p><strong>Status:</strong> {order.status.upper()}</p>
            </div>
            
            <div class="amount-box">
                <div class="amount-label">Amount Due</div>
                <div class="amount-value">${order.total_amount:.2f}</div>
            </div>
            
            <div class="qr-code">
                <img src="{qr_base64}" alt="Payment QR Code">
                <div class="qr-label">📱 Scan to Pay Instantly</div>
            </div>
            
            <div class="payment-id">
                <strong>Payment Reference:</strong> {payment.reference_number}
            </div>
            
            <div class="instructions">
                <strong>How it works:</strong>
                <p style="margin-top: 8px;">Scan this QR code with your mobile device to securely complete the payment for your order.</p>
            </div>
            
            <div class="status-badge {'paid' if order.is_paid else ''}">
                {'✓ Payment Completed' if order.is_paid else '⏳ Payment Pending'}
            </div>
            
            <div class="button-group">
                <a href="/qr/orders/{order_id}/page" class="button secondary">Back to Order</a>
                <a href="/api/v1/orders" class="button">All Orders</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html


@router.get("/payments/{payment_id}/qr", response_class=Response)
def get_payment_qr_code(
    payment_id: int,
    db: Session = Depends(get_db)
):
    """Generate QR code for a payment (scan to pay)."""
    service = PaymentService(db)
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    qr_code = QRCodeService.generate_payment_qr_code(payment_id)
    return Response(
        content=qr_code.getvalue(),
        media_type="image/png"
    )


@router.get("/payments/{payment_id}/qr/page", response_class=HTMLResponse)
def get_payment_qr_page(
    payment_id: int,
    db: Session = Depends(get_db)
):
    """Get a page displaying the scan-to-pay QR code for a payment."""
    service = PaymentService(db)
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    qr_base64 = QRCodeService.generate_payment_qr_code_base64(payment_id)
    status_class = payment.status.lower()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Payment QR Code - Scan to Pay</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .container {{
                background: white;
                border-radius: 10px;
                padding: 40px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                text-align: center;
                max-width: 500px;
            }}
            h1 {{
                color: #333;
                margin-bottom: 10px;
            }}
            .payment-header {{
                font-size: 24px;
                color: #667eea;
                margin: 20px 0;
            }}
            .amount {{
                font-size: 36px;
                font-weight: bold;
                color: #333;
                margin: 20px 0;
            }}
            .details {{
                background: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 30px;
                text-align: left;
            }}
            .detail-item {{
                margin: 10px 0;
            }}
            .detail-label {{
                font-weight: bold;
                color: #667eea;
            }}
            .qr-code {{
                margin: 30px 0;
                padding: 20px;
                background: #f9f9f9;
                border-radius: 5px;
            }}
            .qr-code img {{
                max-width: 300px;
                width: 100%;
                height: auto;
            }}
            .status {{
                padding: 10px;
                border-radius: 5px;
                margin: 15px 0;
                font-weight: bold;
            }}
            .status.pending {{
                background: #fff3cd;
                color: #856404;
            }}
            .status.completed {{
                background: #d1e7dd;
                color: #0f5132;
            }}
            .status.failed {{
                background: #f8d7da;
                color: #842029;
            }}
            .instructions {{
                color: #666;
                font-size: 14px;
                margin-top: 20px;
                background: #e7f3ff;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #667eea;
            }}
            .button {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                cursor: pointer;
                border: none;
                font-size: 14px;
            }}
            .button:hover {{
                background: #764ba2;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Scan to Pay</h1>
            <div class="payment-header">Payment ID: {payment_id}</div>
            <div class="amount">${payment.amount:.2f}</div>
            <div class="details">
                <div class="detail-item">
                    <span class="detail-label">Order ID:</span> {payment.order_id}
                </div>
                <div class="detail-item">
                    <span class="detail-label">Payment Method:</span> {payment.payment_method.replace('_', ' ').title()}
                </div>
                <div class="detail-item">
                    <span class="detail-label">Reference:</span> {payment.reference_number}
                </div>
            </div>
            <div class="status {status_class}">
                Status: {payment.status.upper()}
            </div>
            <div class="qr-code">
                <img src="{qr_base64}" alt="Scan to Pay QR Code">
            </div>
            <div class="instructions">
                <strong>How to use:</strong>
                <p>Scan this QR code with your mobile device to complete the payment securely.</p>
            </div>
            <a href="/api/v1/payments" class="button">Back to Payments</a>
        </div>
    </body>
    </html>
    """
    return html


@router.get("/foods/qr/display", response_class=HTMLResponse)
def display_foods_with_qr():
    """Display all foods with QR code links."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Food Shop - QR Codes</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            h1 {
                color: white;
                text-align: center;
                margin-bottom: 40px;
            }
            .food-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }
            .food-card {
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            }
            .food-name {
                font-size: 20px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            .food-info {
                color: #666;
                font-size: 14px;
                margin-bottom: 15px;
            }
            .button {
                display: inline-block;
                padding: 10px 15px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-size: 13px;
                margin-right: 10px;
            }
            .button:hover {
                background: #764ba2;
            }
            .info-box {
                background: white;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                margin-top: 30px;
            }
            .info-box h2 {
                color: #667eea;
                margin-top: 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Food Shop - QR Code Display</h1>
            
            <div class="info-box">
                <h2>Getting Started</h2>
                <p>Click on "Show QR" button for any food item to display a QR code that customers can scan to view food details.</p>
                <p>You can also access QR codes for payments and orders using their respective endpoints.</p>
            </div>
            
            <div class="food-grid" id="foodGrid">
                <p style="color: white; grid-column: 1/-1; text-align: center;">Loading foods...</p>
            </div>
        </div>
        
        <script>
            fetch('/api/v1/foods')
                .then(response => response.json())
                .then(foods => {
                    const foodGrid = document.getElementById('foodGrid');
                    foodGrid.innerHTML = '';
                    
                    if (foods.length === 0) {
                        foodGrid.innerHTML = '<p style="color: white; grid-column: 1/-1; text-align: center;">No foods available. Create some foods first!</p>';
                        return;
                    }
                    
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
                            <a href="/qr/foods/${food.id}/page" class="button">Show QR Code</a>
                        `;
                        foodGrid.appendChild(card);
                    });
                })
                .catch(error => {
                    document.getElementById('foodGrid').innerHTML = '<p style="color: white; grid-column: 1/-1; text-align: center;">Error loading foods.</p>';
                    console.error('Error:', error);
                });
        </script>
    </body>
    </html>
    """
    return html
