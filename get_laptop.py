import pandas as pd
import re
def laptops(page):
    laptops = []

    laptop_all = page.query_selector_all('div.lvJbLV.col-12-12 div.jIjQ8S')

    for laptop in laptop_all:
        try:
            lp_title = laptop.query_selector('div.RG5Slk').inner_text()
        except:
            lp_title = "N/A"

        try:
            current_price = laptop.query_selector('div.hZ3P6w.DeU9vF').inner_text()
        except:
            current_price = "N/A"

        try:
            original_price = laptop.query_selector('div.kRYCnD.gxR4EY').inner_text()
        except:
            original_price = "N/A"

        try:
            lp_rating = laptop.query_selector('div.MKiFS6').inner_text()
        except:
            lp_rating = "N/A"

        try:
            rating_text = laptop.query_selector('span.PvbNMB').inner_text()
            num_ratings = rating_text.split('Ratings')[0].strip()
            num_reviews = rating_text.split('&')[1].replace('Reviews', '').strip()
        except:
            num_ratings = "N/A"
            num_reviews = "N/A"
        
        try:
            percent_off = laptop.query_selector('div.HQe8jr span').inner_text()
        except:
            percent_off = "N/A"

        try:
            feature_elements = laptop.query_selector_all('div.CMXw7N ul.HwRTzP li.DTBslk')
            features = " | ".join([f.inner_text() for f in feature_elements])
        except:
            features = "N/A"

        # Clean Title: remove last 3 dots if they exist
        lp_title = lp_title.rstrip('.')

        # Clean Prices: Extract numeric value and format with Rupee symbol (₹)
        def format_price(price_str):
            if price_str == "N/A":
                return "N/A"
            # Extract digits and commas using regex
            match = re.search(r'[\d,]+', str(price_str))
            if match:
                return f"₹{match.group()}"
            return price_str
       # Clean Ratings and Reviews: Extract only numeric values
        def format_count(count_str):
            if count_str == "N/A":
                return "N/A"
            match = re.search(r'[\d,]+', str(count_str))
            return match.group() if match else "N/A"

        num_ratings = format_count(num_ratings)
        num_reviews = format_count(num_reviews)

        current_price = format_price(current_price)
        original_price = format_price(original_price)

        # Clean Discount: Extract only the numeric percentage value
        try:
            discount_match = re.search(r'(\d+)%', percent_off)
            percent_off = discount_match.group(1) if discount_match else "N/A"
        except:
            percent_off = "N/A"

        laptops.append({
                "Title": lp_title,
                "Current_Price": current_price,
                "Original_Price": original_price,
                "Discount": percent_off,
                "Rating":lp_rating,
                "Ratings_Count": num_ratings,
                "Reviews_Count": num_reviews,
                "Features": features
            })

    return laptops
