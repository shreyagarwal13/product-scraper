import json
import os 

from database.redis_manager import RedisManager

class DBManager:
    PRODUCT_INFO_FILE_NAME = "scraped_data.json"

    @classmethod
    def save_json_to_file(cls, json_data:dict, file_name: str ='temp.json'):
        with open(file_name, "w") as f:
            json.dump(json_data, f, indent=2)

    @classmethod
    def get_json_from_file(cls, file_name: str ='temp.json'):
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                return json.load(f)
        return []

    @classmethod    
    def save_update_product_info(cls, products: list):
        redis_obj = RedisManager()
        updated_products = {}
        for product in products:
            product_id = product.get("product_title")
            product_cached_info = redis_obj.get_cache(product_id)
            if product_cached_info:
                if product_cached_info.get("product_price")!= product.get("product_price"):
                    print(f"Price changed for {product_id}")
                    updated_products[product_id] = product
                    redis_obj.set_cache(product_id, product)
            else:
                updated_products[product_id] = product
                redis_obj.set_cache(product_id, product)

        file_name = cls.PRODUCT_INFO_FILE_NAME
        if updated_products:
            product_saved_data = cls.get_json_from_file(file_name)
            product_saved_data = {product.get("product_title"): product for product in product_saved_data}

            for product_id in updated_products.keys():
                product_saved_data[product_id] = updated_products.get(product_id)

            final_data = list(product_saved_data.values())
            cls.save_json_to_file(final_data, file_name)
    