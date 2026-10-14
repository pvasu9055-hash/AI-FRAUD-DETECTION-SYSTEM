import os
from dotenv import load_dotenv
load_dotenv()
for k in ["RESEND_API_KEY", "MAIL_FROM", "FLASK_SECRET_KEY", "OTP_EXPIRY_MINUTES"]:
    v = os.getenv(k)
    print(k, "SET" if v else "MISSING", "len", len(v) if v else 0)
import jwt, resend
print("PyJWT", jwt.__version__, "| resend installed OK")
