from src.recharging_data import recharging_data

def main():
    recharging_data("../data/instruction_data_menstable.json", "../data/instruction_parquet.parquet")
    
if __name__ == "__main__":
    main()