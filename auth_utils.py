# ============================================================
# AUTH UTILITIES: JWT tokens, OTP codes, Resend email
# ============================================================

import os
import hmac
import hashlib
import secrets
import html
from datetime import datetime, timedelta, timezone

import jwt
import resend
from dotenv import load_dotenv

load_dotenv()

JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = int(os.environ.get("JWT_EXPIRY_HOURS", "8"))
OTP_EXPIRY_MINUTES = int(os.environ.get("OTP_EXPIRY_MINUTES", "10"))
OTP_MAX_ATTEMPTS = 5

DEV_SECRET = "dev-only-change-this-secret-key"


def _secret():
    return (
        os.environ.get("JWT_SECRET_KEY")
        or os.environ.get("FLASK_SECRET_KEY")
        or DEV_SECRET
    )


# ------------------------------------------------------------
# JWT
# ------------------------------------------------------------

def create_access_token(user_id, name, email):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "name": name,
        "email": email,
        "iat": now,
        "exp": now + timedelta(hours=JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, _secret(), algorithm=JWT_ALGORITHM)


def decode_access_token(token):
    """Return the payload dict, or None if the token is missing, bad or expired."""
    if not token:
        return None
    try:
        return jwt.decode(token, _secret(), algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None


# ------------------------------------------------------------
# OTP
# ------------------------------------------------------------

def generate_otp():
    return f"{secrets.randbelow(1000000):06d}"


def hash_otp(email, otp):
    message = f"{email.lower()}:{otp}".encode("utf-8")
    return hmac.new(_secret().encode("utf-8"), message, hashlib.sha256).hexdigest()


def verify_otp_hash(email, otp, stored_hash):
    return hmac.compare_digest(hash_otp(email, otp), stored_hash or "")


# ------------------------------------------------------------
# EMAIL (Resend)
# ------------------------------------------------------------

def send_otp_email(to_email, name, otp, purpose):
    """Send the OTP email. Returns (True, None) or (False, error_message)."""
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        return False, "RESEND_API_KEY is not set"

    resend.api_key = api_key
    sender = os.environ.get("MAIL_FROM", "FraudShield <onboarding@resend.dev>")
    action = "complete your registration" if purpose == "register" else "sign in"
    safe_name = html.escape(name or "there")

    body = f"""
    <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;padding:24px;">
      <h2 style="color:#0f172a;">FraudShield verification code</h2>
      <p>Hi {safe_name},</p>
      <p>Use this code to {action}:</p>
      <p style="font-size:34px;font-weight:800;letter-spacing:8px;color:#2563eb;">{otp}</p>
      <p>This code expires in {OTP_EXPIRY_MINUTES} minutes. If you did not request it, ignore this email.</p>
    </div>
    """

    try:
        resend.Emails.send({
            "from": sender,
            "to": [to_email],
            "subject": f"Your FraudShield code: {otp}",
            "html": body,
        })
        return True, None
    except Exception as exc:
        return False, str(exc)
