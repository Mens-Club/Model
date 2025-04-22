from src.category_generate import recommend_by_filter, get_season_category_map

clothes = get_season_category_map(
    table_name="menstable",
    category_column="main_category",
    save_path="../data/season_category_filter.json"
)

shoes = get_season_category_map(
    table_name="shoes_test",
    fixed_category="신발",
    save_path="../data/season_category_filter_shoes.json"
)
