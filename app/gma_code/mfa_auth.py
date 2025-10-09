import io, base64
from urllib.parse import quote
from typing import Optional
import boto3
import qrcode
from fastapi import HTTPException, Body

REGION = "ap-southeast-2"
DEFAULT_ISSUER = "GifMakerApp"
DEFAULT_LABEL  = "CognitoUser"

def _cognito():
    return boto3.client("cognito-idp", region_name=REGION)

def _qr_png_b64(otpauth_uri: str) -> str:
    img = qrcode.make(otpauth_uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def _build_otpauth(secret: str, issuer: str, label: str) -> str:
    iss = quote(issuer, safe="")
    lab = quote(label,  safe="")
    return (
        f"otpauth://totp/{iss}:{lab}"
        f"?secret={secret}&issuer={iss}&algorithm=SHA1&digits=6&period=30"
    )

def _pick_ctx(*, access_token: Optional[str], session: Optional[str]) -> tuple[str, str]:
    """
    Prefer 'session' when both are present (e.g., during MFA_SETUP_REQUIRED),
    otherwise fall back to 'access_token'. Error only if neither provided.
    """
    if session:
        return ("session", session)
    if access_token:
        return ("access_token", access_token)
    from fastapi import HTTPException
    raise HTTPException(status_code=400, detail="Provide session or access_token")

# ----------------- public endpoints -----------------

def associate_totp(
    access_token: Optional[str] = Body(None, embed=True),
    session: Optional[str]      = Body(None, embed=True),
    issuer: str                 = Body(DEFAULT_ISSUER, embed=True),
    label: str                  = Body(DEFAULT_LABEL,  embed=True),
):
    """
    Start TOTP setup. Accepts either:
      - { "access_token": "<AccessToken>" }    # optional MFA pools
      - { "session": "<Session>" }             # MFA_SETUP challenge
    Returns: { ok, secret, context, otpauth_uri, qrcode_png_base64, [session] }
    """
    key, ctx = _pick_ctx(access_token=access_token, session=session)
    client = _cognito()
    try:
        if key == "access_token":
            r = client.associate_software_token(AccessToken=ctx)
        else:
            r = client.associate_software_token(Session=ctx)

        secret = r["SecretCode"]
        session_out = r.get("Session", session)  # only present on session path

        otpauth = _build_otpauth(secret, issuer, label)
        return {
            "ok": True,
            "secret": secret,
            "context": key,  # "access_token" or "session"
            "otpauth_uri": otpauth,
            "qrcode_png_base64": _qr_png_b64(otpauth),
            **({"session": session_out} if session_out else {}),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"AssociateSoftwareToken failed: {e}")

def verify_totp(
    code: str                   = Body(...,  embed=True),
    access_token: Optional[str] = Body(None, embed=True),
    session: Optional[str]      = Body(None, embed=True),
):
    """
    Verify a 6-digit code. Accepts either:
      - { "access_token": "<AccessToken>", "code": "123456" }
      - { "session": "<Session>", "code": "123456" }
    Returns: { ok, status, [session] }
    """
    key, ctx = _pick_ctx(access_token=access_token, session=session)
    client = _cognito()
    try:
        if key == "access_token":
            r = client.verify_software_token(AccessToken=ctx, UserCode=code, FriendlyDeviceName="TOTP")
        else:
            r = client.verify_software_token(Session=ctx, UserCode=code, FriendlyDeviceName="TOTP")

        status = r.get("Status", "ERROR")
        return {
            "ok": status == "SUCCESS",
            "status": status,
            **({"session": r.get("Session")} if r.get("Session") else {}),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"VerifySoftwareToken failed: {e}")

def set_totp_preferred(
    access_token: str = Body(..., embed=True),
    enable: bool      = Body(True, embed=True),
):
    """
    Enable/disable Software TOTP as preferred MFA factor (requires AccessToken).
    Body: { "access_token": "<AccessToken>", "enable": true }
    Returns: { ok: true }
    """
    client = _cognito()
    try:
        client.set_user_mfa_preference(
            SoftwareTokenMfaSettings={"Enabled": enable, "PreferredMfa": enable},
            AccessToken=access_token,
        )
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SetUserMFAPreference failed: {e}")
