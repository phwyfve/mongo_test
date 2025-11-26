from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.manager import BaseUserManager
from fastapi import Depends, Request
from models import User, get_user_db
from config import settings
from typing import Optional
from beanie import PydanticObjectId
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class UserManager(BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = settings.secret_key
    verification_token_secret = settings.secret_key

    def parse_id(self, value) -> PydanticObjectId:
        """Parse string ID to PydanticObjectId"""
        if isinstance(value, PydanticObjectId):
            return value
        return PydanticObjectId(value)

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        print(f"Hello my friend {user.first_name or user.email}, welcome to our platform!")
        
        # Only request verification if user is not already verified
        if not user.is_verified:
            print(f"User {user.email} needs verification. Sending verification email...")
            await self.request_verify(user, request)
        else:
            print(f"User {user.email} is already verified. No verification email needed.")

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        print(f"=== VERIFICATION EMAIL ===")
        print(f"To: {user.email}")
        print(f"Subject: Hello my friend, verify your email!")
        print(f"Message: Hello my friend {user.first_name or 'there'}, click on that link and grow my user base!")
        print(f"Verification URL: http://localhost:8000/auth/verify?token={token}")
        print("========================")
        
        # Send actual email (uncomment to enable)
        await self.send_verification_email(user, token)
    
    async def send_verification_email(self, user: User, token: str):
        """Send verification email using SMTP or email service"""
        try:
            verify_url = f"http://localhost:8000/auth/verify?token={token}"
            
            # Option 1: Gmail SMTP (for development)
            # msg = MIMEMultipart()
            # msg['From'] = "your-email@gmail.com" 
            # msg['To'] = user.email
            # msg['Subject'] = "Hello my friend, verify your email!"
            # 
            # body = f"Hello my friend {user.first_name or 'there'},\n\nClick on that link and grow my user base!\n{verify_url}"
            # msg.attach(MIMEText(body, 'plain'))
            # 
            # with smtplib.SMTP('smtp.gmail.com', 587) as server:
            #     server.starttls()
            #     server.login("your-email@gmail.com", "your-app-password")
            #     server.send_message(msg)
            
            # Option 2: SendGrid API (recommended for production)
            # import sendgrid
            # from sendgrid.helpers.mail import Mail
            # 
            # sg = sendgrid.SendGridAPIClient(api_key=settings.sendgrid_api_key)
            # message = Mail(
            #     from_email='noreply@yourapp.com',
            #     to_emails=user.email,
            #     subject='Hello my friend, verify your email!',
            #     html_content=f'<p>Hello my friend {user.first_name or "there"},</p><p><a href="{verify_url}">Click on that link and grow my user base!</a></p>'
            # )
            # sg.send(message)
            
            print(f"✅ Email would be sent to {user.email} (email sending disabled for demo)")
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
        
    async def on_after_verify(self, user: User, request: Optional[Request] = None):
        print(f"User {user.email} has been verified! Welcome to the family!")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[any] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


# JWT Strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret_key, lifetime_seconds=3600)


# Authentication Backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)

# FastAPI Users instance
fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

# Current user dependencies
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
