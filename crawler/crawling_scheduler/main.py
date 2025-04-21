from get_category import connect_to_db, get_categories
from generate_url import generate_url
from send_requests import send_requests
from push_to_db import push_to_db

categories = get_categories(connect_to_db())
shoes_urls, bottom_urls, outwear_urls, top_urls = generate_url(categories)
shoes_results, other_results = send_requests(shoes_urls, bottom_urls, outwear_urls, top_urls)
push_to_db(connect_to_db(), shoes_results, other_results)