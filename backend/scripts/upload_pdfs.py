import os
import glob
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from the parent directory's .env file
# Assuming script is run from backend/ or backend/scripts/
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env")
    exit(1)

supabase: Client = create_client(url, key)

NOTES_DIR = "/Users/8teen/Downloads/04_/Active/GrindOS/notes/output"
BUCKET_NAME = "grindos-documents"

def upload_pdfs():
    print(f"Starting upload of PDFs from {NOTES_DIR} to bucket '{BUCKET_NAME}'...")
    
    # Verify bucket exists (optional, but good practice)
    try:
        buckets = supabase.storage.list_buckets()
        bucket_names = [b.name for b in buckets]
        if BUCKET_NAME not in bucket_names:
            print(f"WARNING: Bucket '{BUCKET_NAME}' does not exist! Please create it in the Supabase Dashboard.")
            return
    except Exception as e:
        print(f"Failed to check buckets (you may not have admin rights with this key, proceeding anyway): {e}")

    pdf_files = glob.glob(os.path.join(NOTES_DIR, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {NOTES_DIR}")
        return

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"Uploading {filename}...")
        
        with open(pdf_path, 'rb') as f:
            try:
                # We upload to the root of the bucket with the same filename
                res = supabase.storage.from_(BUCKET_NAME).upload(
                    file=f,
                    path=filename,
                    file_options={"content-type": "application/pdf"}
                )
                print(f"✅ Successfully uploaded {filename}")
            except Exception as e:
                # Supabase raises an error if file already exists
                if "Duplicate" in str(e) or "already exists" in str(e).lower() or getattr(e, "code", None) == "409" or "The resource already exists" in str(e):
                    print(f"⚠️ {filename} already exists in bucket.")
                else:
                    print(f"❌ Failed to upload {filename}: {e}")

if __name__ == "__main__":
    upload_pdfs()
