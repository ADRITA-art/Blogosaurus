import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

def test_connection():
    """Test the database connection directly with psycopg2."""
    try:
        # Get DATABASE_URL from environment
        db_url = os.environ.get('DATABASE_URL')
        
        if not db_url:
            print("ERROR: DATABASE_URL not found in environment variables.")
            return False
        
        # Check if the URL has the full hostname format
        if 'oregon-postgres.render.com' not in db_url and 'dpg-' in db_url:
            # Extract the database ID part
            parts = db_url.split('@')
            if len(parts) > 1:
                prefix = parts[0] + '@'
                rest = parts[1].split('/')
                hostname = rest[0]
                suffix = '/' + '/'.join(rest[1:]) if len(rest) > 1 else ''
                
                # Add the domain suffix if missing
                if not hostname.endswith('.oregon-postgres.render.com'):
                    hostname += '.oregon-postgres.render.com'
                
                # Reconstruct the URL
                corrected_db_url = prefix + hostname + suffix
                print(f"Original URL appears incomplete. Trying corrected URL: {corrected_db_url}")
                db_url = corrected_db_url
        
        print(f"Trying to connect to: {db_url}")
        
        # Connect to the database
        conn = psycopg2.connect(db_url)
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute a simple query
        cur.execute('SELECT version();')
        
        # Get the result
        version = cur.fetchone()
        print(f"Connection successful! PostgreSQL version: {version[0]}")
        
        # Close cursor and connection
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Connection failed with error: {e}")
        
        # Check if the error is related to host resolution
        if "could not translate host name" in str(e):
            print("\nSuggestions:")
            print("1. Check if your DATABASE_URL hostname is correct")
            print("2. If using render.com, ensure the format is: dpg-xxxxx.oregon-postgres.render.com")
            print("3. Try pinging the host to check if it's reachable")
            
        return False

if __name__ == "__main__":
    print("-" * 80)
    print("Testing PostgreSQL Connection")
    print("-" * 80)
    success = test_connection()
    print("-" * 80)
    if success:
        print("✅ Connection test PASSED")
    else:
        print("❌ Connection test FAILED")
    print("-" * 80)
