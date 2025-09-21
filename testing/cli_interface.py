from gma_code import auth
from testing import Python_Testing_Collection as ptc
from gma_code import secrets_loader

def interactive_auth():
    global user_1_auth, current_username
    choice = input("Choose [S]ign up or [L]og in: ").strip().lower()

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

        tokens = auth.authenticate(username=username, password=password)
        if not tokens or "AccessToken" not in tokens:
            print("Login failed after signup.")
            return False
        user_1_auth = {"Authorization": f"Bearer {tokens['AccessToken']}"}
        print("Auth header set.")
        return True

    else:  # login
        username = input("Enter username: ").strip()
        password = input("Enter password: ")
        current_username = username

        tokens = auth.authenticate(username=username, password=password)
        if not tokens or "AccessToken" not in tokens:
            print("Login failed — check credentials or confirm your account.")
            return False
        user_1_auth = {"Authorization": f"Bearer {tokens['AccessToken']}"}
        print("Auth header set.")
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
    print("5) Get all GIFs")
    print("6) Download gif (fixed name)")
    print("7) Upload to GIPHY (fixed name)")
    print("8) Download from GIPHY by ID")
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
            ptc.convert_to_gif(f"{current_username}_hummingbird_images", "hummingbird_gif")
        elif choice == "5":
            ptc.get_all_gifs(1, False)
        elif choice == "6":
            ptc.download_gif()
        elif choice == "7":
            ptc.upload_to_GIPHY()
        elif choice == "8":
            ptc.download_from_GIPHY(secrets_loader.get_secret("A2_Group11-GIPHY")["GIPHY_API"])
        elif choice == "9":
            print("Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()