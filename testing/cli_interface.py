from gma_code import auth
from testing import Python_Testing_Collection as ptc
from gma_code import mfa_auth
import os, base64

LOGIN_USERNAME = os.getenv("LOGIN_USERNAME", "")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "")

# Remember to change API_HOST in Python_Testing_Collection to container address before running script

LOGIN_USERNAME = os.getenv("LOGIN_USERNAME", "")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "")

def interactive_auth():
    global user_1_auth, current_username
    choice = input("Choose [S]ign up, [L]og in, or [U]se env credentials to login: ").strip().lower()

    def _complete_login(username: str, password: str):
        """Handles tokens, TOTP challenge, and first-time MFA setup (session-based)."""
        res = auth.authenticate(username=username, password=password)

        # Case A: direct tokens (either raw tokens dict, or status=OK)
        if isinstance(res, dict) and "AccessToken" in res:
            return res
        if isinstance(res, dict) and res.get("status") == "OK" and "tokens" in res:
            return res["tokens"]

        # Case B: a known challenge
        if isinstance(res, dict) and res.get("status") in {"TOTP_REQUIRED", "MFA_SETUP_REQUIRED"}:
            status  = res["status"]
            session = res.get("session")

            if status == "TOTP_REQUIRED":
                code = input("Enter 6-digit TOTP code: ").strip()
                r = auth.respond_totp(session=session, username=username, code=code)
                if isinstance(r, dict) and r.get("status") == "OK":
                    return r["tokens"]
                print("TOTP verification failed.")
                return None

            if status == "MFA_SETUP_REQUIRED":
                # 1) Associate using Session (not AccessToken)
                assoc = mfa_auth.associate_totp(session=session, issuer="GifMakerApp", label=username)
                secret   = assoc["secret"]
                session2 = assoc.get("session", session)

                print("\nScan this in your authenticator app, then enter the first 6-digit code:")
                print(assoc["otpauth_uri"])

                # Optionally write the QR PNG to disk for easy scanning
                qr_b64 = assoc.get("qrcode_png_base64")
                if qr_b64:
                    with open("mfa_qr.png", "wb") as f:
                        f.write(base64.b64decode(qr_b64))
                    print("Saved QR to mfa_qr.png")

                # 2) Verify first code using Session
                code1 = input("First 6-digit code: ").strip()
                ver = mfa_auth.verify_totp(session=session2, code=code1)
                if not ver.get("ok"):
                    print("TOTP verification failed.")
                    return None

                # 3) Re-initiate auth; now user will get SOFTWARE_TOKEN_MFA
                res2 = auth.authenticate(username=username, password=password)
                if isinstance(res2, dict) and res2.get("status") == "TOTP_REQUIRED":
                    code2 = input("Enter 6-digit code to complete sign-in: ").strip()
                    r2 = auth.respond_totp(session=res2.get("session"), username=username, code=code2)
                    if isinstance(r2, dict) and r2.get("status") == "OK":
                        return r2["tokens"]
                    print("Final TOTP step failed.")
                    return None

                # Or direct tokens (some pools issue tokens after verify)
                if isinstance(res2, dict) and "AccessToken" in res2:
                    return res2
                if isinstance(res2, dict) and res2.get("status") == "OK" and "tokens" in res2:
                    return res2["tokens"]

                print(f"Unexpected post-setup response: {res2}")
                return None

        # Case C: error or unexpected shape
        detail = (res or {}).get("detail") if isinstance(res, dict) else str(res)
        print(f"Login failed — {detail or 'unknown error'}")
        return None

    # ----- sign up path -----
    if choice.startswith("s"):
        username = input("Enter username: ").strip()
        email    = input("Enter email: ").strip()
        password = input("Enter password: ")
        current_username = username

        signup_resp = auth.signup(username=username, email=email, password=password)
        if not signup_resp:
            print("Signup failed (user may already exist). Try login.")
            return False
        print("Signup:", signup_resp)
        if not signup_resp.get("UserConfirmed", False):
            code = input("Enter confirmation code from email: ").strip()
            try:
                confirm_resp = auth.confirm_user(username=username, code=code)
                print("Confirm:", confirm_resp)
            except Exception as e:
                print(f"Confirmation failed: {e}")
                return False

        tokens = _complete_login(username, password)
        if not tokens or "AccessToken" not in tokens:
            print("Login failed after signup.")
            return False
        user_1_auth = {"Authorization": f"Bearer {tokens['AccessToken']}"}
        ptc.user_1_auth = user_1_auth
        print("Auth header set: " + user_1_auth["Authorization"])
        return True

    # ----- login path -----
    else:
        username = LOGIN_USERNAME
        password = LOGIN_PASSWORD
        if choice.startswith("l"):
            username = input("Enter username: ").strip()
            password = input("Enter password: ")
        current_username = username

        tokens = _complete_login(username, password)
        if not tokens or "AccessToken" not in tokens:
            return False
        user_1_auth = {"Authorization": f"Bearer {tokens['AccessToken']}"}
        ptc.user_1_auth = user_1_auth
        print("Auth header set: " + user_1_auth["Authorization"])
        return True
        


# ---------------------------
# Menu
# ---------------------------
def menu():
    print("\n== Actions ==")
    print("1) Upload test images")
    print("2) Upload load images")
    print("3) Get all images")
    print("4) Convert to GIF")
    print("5) Convert to GIF repeatedly (for CPU load)")
    print("6) Get all GIFs")
    print("7) Download gif (fixed name)")
    print("8) Upload to GIPHY (fixed name)")
    print("9) Exit")
    return input("Choose: ").strip()

def main():
    if not interactive_auth():
        return

    while True:
        choice = menu()
        # Require auth header
        if not user_1_auth and choice != "9":
            print("Not authorized yet. Please restart and log in.")
            break

        if choice == "1":
            ptc.upload_test_images()
        elif choice == "2":
            ptc.upload_load_images()
        elif choice == "3":
            ptc.get_all_images()
        elif choice == "4":
            ptc.convert_to_gif(images_name=f"{current_username}_hummingbird".lower(), gif_name="hummingbird")
        elif choice == "5":
            for i in range(100):
                ptc.convert_to_gif(images_name=f"{current_username}_load".lower(), gif_name="load_" + str(i))
        elif choice == "6":
            ptc.get_all_gifs(1, False)
        elif choice == "7":
            ptc.download_gif()
        elif choice == "8":
            ptc.upload_to_GIPHY()
        elif choice == "9":
            print("Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()