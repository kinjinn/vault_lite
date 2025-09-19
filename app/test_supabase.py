from supabase_client import supabase

def main():
    response = supabase.table("test_table").select("*").execute()
    print("error:", getattr(response, "error", None))
    print("data:", response.data)

if __name__ == "__main__":
    main()