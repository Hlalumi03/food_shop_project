import io
import qrcode
from PIL import Image
from typing import Optional
from app.core.config import settings


class QRCodeService:
    """Service for generating QR codes for payment and product pages."""
    
    @staticmethod
    def generate_qr_code(
        data: str,
        size: int = 10,
        border: int = 2,
        format: str = "PNG"
    ) -> io.BytesIO:
        """
        Generate a QR code and return as BytesIO object.
        
        Args:
            data: The data to encode in the QR code (URL or text)
            size: The size of each box in pixels
            border: The border size in boxes
            format: The image format (PNG, JPEG, etc.)
        
        Returns:
            BytesIO object containing the QR code image
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to BytesIO
        img_bytes = io.BytesIO()
        img.save(img_bytes, format=format)
        img_bytes.seek(0)
        
        return img_bytes
    
    @staticmethod
    def generate_qr_code_base64(
        data: str,
        size: int = 10,
        border: int = 2
    ) -> str:
        """
        Generate a QR code and return as base64 string for embedding in HTML.
        
        Args:
            data: The data to encode in the QR code
            size: The size of each box in pixels
            border: The border size in boxes
        
        Returns:
            Base64 encoded string of the QR code image
        """
        import base64
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
        return f"data:image/png;base64,{img_base64}"
    
    @staticmethod
    def generate_food_qr_code(food_id: int) -> io.BytesIO:
        """Generate QR code for a food item."""
        url = f"{settings.API_BASE_URL}/foods/{food_id}"
        return QRCodeService.generate_qr_code(url)
    
    @staticmethod
    def generate_food_qr_code_base64(food_id: int) -> str:
        """Generate QR code for a food item as base64."""
        url = f"{settings.API_BASE_URL}/foods/{food_id}"
        return QRCodeService.generate_qr_code_base64(url)
    
    @staticmethod
    def generate_payment_qr_code(payment_id: int) -> io.BytesIO:
        """Generate QR code for a payment (scan-to-pay)."""
        url = f"{settings.API_BASE_URL}/pay/{payment_id}"
        return QRCodeService.generate_qr_code(url)
    
    @staticmethod
    def generate_payment_qr_code_base64(payment_id: int) -> str:
        """Generate QR code for a payment as base64."""
        url = f"{settings.API_BASE_URL}/pay/{payment_id}"
        return QRCodeService.generate_qr_code_base64(url)
    
    @staticmethod
    def generate_order_qr_code(order_id: int) -> io.BytesIO:
        """Generate QR code for an order."""
        url = f"{settings.API_BASE_URL}/orders/{order_id}"
        return QRCodeService.generate_qr_code(url)
    
    @staticmethod
    def generate_order_qr_code_base64(order_id: int) -> str:
        """Generate QR code for an order as base64."""
        url = f"{settings.API_BASE_URL}/orders/{order_id}"
        return QRCodeService.generate_qr_code_base64(url)

    @staticmethod
    def generate_website_qr_code() -> io.BytesIO:
        """Generate QR code that points to the website root."""
        url = f"{settings.API_BASE_URL}/"
        return QRCodeService.generate_qr_code(url)

    @staticmethod
    def generate_website_qr_code_base64() -> str:
        """Generate QR code for the website root as base64."""
        url = f"{settings.API_BASE_URL}/"
        return QRCodeService.generate_qr_code_base64(url)
