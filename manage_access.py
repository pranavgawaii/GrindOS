#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error
import urllib.parse

# Load env variables manually from backend/.env
def load_env_manually(path):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                # Strip potential surrounding quotes from values
                val_clean = val.strip().strip("'").strip('"')
                os.environ[key.strip()] = val_clean

env_path = os.path.join(os.path.dirname(__file__), "backend", ".env")
load_env_manually(env_path)

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

if not CLERK_SECRET_KEY:
    print("❌ Error: CLERK_SECRET_KEY not found in backend/.env")
    sys.exit(1)

def make_request(url, method="GET", payload=None):
    headers = {
        "Authorization": f"Bearer {CLERK_SECRET_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "GrindOS-Admin-CLI"
    }
    
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = response.read().decode("utf-8")
            return status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8")
        try:
            return status, json.loads(body)
        except:
            return status, {"error": body}
    except urllib.error.URLError as e:
        return 0, {"error": str(e.reason)}

def enable_restricted():
    print("⏳ Enabling Restricted Mode (Invite-Only)...")
    url = "https://api.clerk.com/v1/instance/restrictions"
    payload = {
        "restricted_to_allowlist": True
    }
    status, res = make_request(url, method="PATCH", payload=payload)
    if status == 200:
        print("✅ Restricted Mode enabled successfully! Only invited users can sign up now.")
    else:
        print(f"❌ Failed to enable Restricted Mode: {status} - {json.dumps(res)}")

def disable_restricted():
    print("⏳ Disabling Restricted Mode (Public Sign-ups)...")
    url = "https://api.clerk.com/v1/instance/restrictions"
    payload = {
        "restricted_to_allowlist": False
    }
    status, res = make_request(url, method="PATCH", payload=payload)
    if status == 200:
        print("✅ Restricted Mode disabled. Anyone can sign up now.")
    else:
        print(f"❌ Failed to disable Restricted Mode: {status} - {json.dumps(res)}")

def invite(email):
    print(f"⏳ Inviting email: {email}...")
    url = "https://api.clerk.com/v1/invitations"
    payload = {
        "email_address": email,
        "notify": True
    }
    status, res = make_request(url, method="POST", payload=payload)
    if status == 200:
        print(f"✅ Invitation sent successfully to {email}!")
        print(f"   ID: {res.get('id')}")
        print(f"   Expires: {res.get('created_at')} (Valid for 30 days)")
    elif status == 422:
        print(f"❌ Invitation failed: User or invitation already exists for {email}.")
    else:
        print(f"❌ Failed to invite user: {status} - {json.dumps(res)}")

def list_invitations():
    print("⏳ Fetching invitations...")
    url = "https://api.clerk.com/v1/invitations"
    status, res = make_request(url, method="GET")
    if status == 200:
        invitations = res
        if not invitations:
            print("ℹ️ No active or pending invitations found.")
            return
        print(f"\n{ 'Email Address':<35} | { 'Status':<10} | { 'ID':<30}")
        print("-" * 81)
        for inv in invitations:
            print(f"{inv.get('email_address'):<35} | {inv.get('status'):<10} | {inv.get('id'):<30}")
    else:
        print(f"❌ Failed to list invitations: {status} - {json.dumps(res)}")

def revoke(email):
    print(f"⏳ Revoking pending invitation for {email}...")
    url = "https://api.clerk.com/v1/invitations"
    status, res = make_request(url, method="GET")
    if status != 200:
        print(f"❌ Failed to query invitations: {status} - {json.dumps(res)}")
        return
    
    invitations = res
    target_id = None
    for inv in invitations:
        if inv.get("email_address") == email and inv.get("status") == "pending":
            target_id = inv.get("id")
            break
            
    if not target_id:
        print(f"❌ Error: No pending invitation found for {email}.")
        return
        
    revoke_url = f"https://api.clerk.com/v1/invitations/{target_id}/revoke"
    status, res = make_request(revoke_url, method="POST")
    if status == 200:
        print(f"✅ Invitation for {email} revoked successfully.")
    else:
        print(f"❌ Failed to revoke invitation: {status} - {json.dumps(res)}")

def ban(email):
    print(f"⏳ Searching for user account with email {email} to ban...")
    url = "https://api.clerk.com/v1/users"
    params = urllib.parse.urlencode({"query": email})
    status, res = make_request(f"{url}?{params}", method="GET")
    if status != 200:
        print(f"❌ Failed to query users: {status} - {json.dumps(res)}")
        return
        
    users = res
    target_user_id = None
    for u in users:
        for mail in u.get("email_addresses", []):
            if mail.get("email_address") == email:
                target_user_id = u.get("id")
                break
        if target_user_id:
            break
            
    if not target_user_id:
        print(f"❌ Error: No registered user found with email {email}.")
        return
        
    ban_url = f"https://api.clerk.com/v1/users/{target_user_id}/ban"
    status, res = make_request(ban_url, method="POST")
    if status == 200:
        print(f"✅ User {email} has been BANNED successfully. Their sessions have been terminated.")
    else:
        print(f"❌ Failed to ban user: {status} - {json.dumps(res)}")

def unban(email):
    print(f"⏳ Searching for user account with email {email} to unban...")
    url = "https://api.clerk.com/v1/users"
    params = urllib.parse.urlencode({"query": email})
    status, res = make_request(f"{url}?{params}", method="GET")
    if status != 200:
        print(f"❌ Failed to query users: {status} - {json.dumps(res)}")
        return
        
    users = res
    target_user_id = None
    for u in users:
        for mail in u.get("email_addresses", []):
            if mail.get("email_address") == email:
                target_user_id = u.get("id")
                break
        if target_user_id:
            break
            
    if not target_user_id:
        print(f"❌ Error: No registered user found with email {email}.")
        return
        
    unban_url = f"https://api.clerk.com/v1/users/{target_user_id}/unban"
    status, res = make_request(unban_url, method="POST")
    if status == 200:
        print(f"✅ User {email} has been UNBANNED successfully.")
    else:
        print(f"❌ Failed to unban user: {status} - {json.dumps(res)}")

# ── Waitlist management methods ──────────────────────────────────────────────

def list_waitlist():
    print("⏳ Fetching waitlist entries...")
    url = "https://api.clerk.com/v1/waitlist_entries"
    status, res = make_request(url, method="GET")
    if status == 200:
        entries = res.get("data", []) if isinstance(res, dict) else res
        if not entries:
            print("ℹ️ No waitlist entries found.")
            return
            
        pending_entries = [e for e in entries if e.get("status") == "pending"]
        if not pending_entries:
            print("ℹ️ No pending waitlist entries found.")
            return
            
        print(f"\n{ 'Email Address':<35} | { 'Status':<10} | { 'ID':<30}")
        print("-" * 81)
        for e in pending_entries:
            email = e.get("email_address") or (e.get("identifier") if "identifier" in e else "—")
            print(f"{email:<35} | {e.get('status'):<10} | {e.get('id'):<30}")
    else:
        print(f"❌ Failed to list waitlist entries: {status} - {json.dumps(res)}")

def approve_waitlist(email):
    print(f"⏳ Searching waitlist for email: {email}...")
    url = "https://api.clerk.com/v1/waitlist_entries"
    status, res = make_request(url, method="GET")
    if status != 200:
        print(f"❌ Failed to query waitlist: {status} - {json.dumps(res)}")
        return
        
    entries = res.get("data", []) if isinstance(res, dict) else res
    target_id = None
    for e in entries:
        curr_email = e.get("email_address") or (e.get("identifier") if "identifier" in e else "")
        if curr_email == email and e.get("status") == "pending":
            target_id = e.get("id")
            break
            
    if not target_id:
        print(f"❌ Error: No pending waitlist entry found for {email}.")
        return
        
    print(f"⏳ Approving & inviting waitlist entry {target_id}...")
    approve_url = f"https://api.clerk.com/v1/waitlist_entries/{target_id}/invite"
    status, res = make_request(approve_url, method="POST")
    if status == 200:
        print(f"✅ Waitlist entry for {email} has been approved and invited!")
    else:
        print(f"❌ Failed to approve waitlist entry: {status} - {json.dumps(res)}")

def reject_waitlist(email):
    print(f"⏳ Searching waitlist for email: {email}...")
    url = "https://api.clerk.com/v1/waitlist_entries"
    status, res = make_request(url, method="GET")
    if status != 200:
        print(f"❌ Failed to query waitlist: {status} - {json.dumps(res)}")
        return
        
    entries = res.get("data", []) if isinstance(res, dict) else res
    target_id = None
    for e in entries:
        curr_email = e.get("email_address") or (e.get("identifier") if "identifier" in e else "")
        if curr_email == email and e.get("status") == "pending":
            target_id = e.get("id")
            break
            
    if not target_id:
        print(f"❌ Error: No pending waitlist entry found for {email}.")
        return
        
    print(f"⏳ Rejecting waitlist entry {target_id}...")
    reject_url = f"https://api.clerk.com/v1/waitlist_entries/{target_id}/reject"
    status, res = make_request(reject_url, method="POST")
    if status == 200:
        print(f"✅ Waitlist entry for {email} has been rejected.")
    else:
        print(f"❌ Failed to reject waitlist entry: {status} - {json.dumps(res)}")

def main():
    if len(sys.argv) < 2:
        print("🛠️  GrindOS Access Control Admin CLI (Clerk)")
        print("\nUsage:")
        print("  python3 manage_access.py enable-restricted     Enable Restricted Mode (Invite-Only sign-ups)")
        print("  python3 manage_access.py disable-restricted    Disable Restricted Mode (Public sign-ups)")
        print("  python3 manage_access.py invite <email>        Approve & send sign-up invitation to email")
        print("  python3 manage_access.py list-invitations      List all pending and accepted invitations")
        print("  python3 manage_access.py revoke <email>        Revoke a pending invitation")
        print("  python3 manage_access.py ban <email>           Ban an existing registered user")
        print("  python3 manage_access.py unban <email>         Unban a banned user")
        print("\nWaitlist Mode Commands:")
        print("  python3 manage_access.py list-waitlist         List pending waitlist sign-ups")
        print("  python3 manage_access.py approve-waitlist <e>  Approve & invite a user on the waitlist")
        print("  python3 manage_access.py reject-waitlist <e>   Reject a user on the waitlist")
        sys.exit(0)
        
    cmd = sys.argv[1]
    
    if cmd == "enable-restricted":
        enable_restricted()
    elif cmd == "disable-restricted":
        disable_restricted()
    elif cmd == "invite":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify the email to invite.")
            sys.exit(1)
        invite(sys.argv[2])
    elif cmd == "list-invitations":
        list_invitations()
    elif cmd == "revoke":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify the email to revoke.")
            sys.exit(1)
        revoke(sys.argv[2])
    elif cmd == "ban":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify the email to ban.")
            sys.exit(1)
        ban(sys.argv[2])
    elif cmd == "unban":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify the email to unban.")
            sys.exit(1)
        unban(sys.argv[2])
    elif cmd == "list-waitlist":
        list_waitlist()
    elif cmd == "approve-waitlist":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify the email to approve.")
            sys.exit(1)
        approve_waitlist(sys.argv[2])
    elif cmd == "reject-waitlist":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify the email to reject.")
            sys.exit(1)
        reject_waitlist(sys.argv[2])
    else:
        print(f"❌ Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
