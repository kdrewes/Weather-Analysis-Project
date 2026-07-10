from Database import Run_Schema
from Dao import main as load_main

def main() -> None:
    
    # Execute schema
    Run_Schema("schema.sql")
    load_main()

if __name__ == "__main__":
    main()