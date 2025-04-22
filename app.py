from flask import Flask, render_template, request, jsonify
import random
import time
import logging
import datetime
import urllib.parse

# Initialize Flask application with new name
app = Flask(__name__, static_folder="static")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PriceX")  # Changed from PriceSync to PriceX

# Generate realistic price history data for the last 6 months
def generate_price_history(base_price, volatility=0.05, months=6):
    history = []
    today = datetime.datetime.now()
    
    for i in range(months):
        date = today - datetime.timedelta(days=30 * (months - i - 1))
        # Create some random price fluctuations
        variation = random.uniform(-volatility, volatility)
        price = int(base_price * (1 + variation))
        history.append({
            'date': date.strftime('%Y-%m-%d'),
            'price': price
        })
    
    return history

# Sample product database with price history
SAMPLE_PRODUCTS = {
    'iphone 15': [
        {
            'title': 'Apple iPhone 15 (128GB) - Blue',
            'price': 61390,
            'price_history': generate_price_history(61390, 0.08),
            'url': 'https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX2F5QT',
            'source': 'Amazon'
        },
        {
            'title': 'APPLE iPhone 15 (Blue, 128 GB)',
            'price': 64400,
            'price_history': generate_price_history(64400, 0.06),
            'url': 'https://www.flipkart.com/apple-iphone-15-black-128-gb/p/itm6ac6485515ae4?pid=MOBGTAGPTB3VS24W&lid=LSTMOBGTAGPTB3VS24WCTBCFM&marketplace=FLIPKART&q=iphone+15&store=tyy%2F4io&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_3_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_3_3_na_na_na&fm=organic&iid=9e43d0f0-9bf0-4810-80df-41150cb9a2cc.MOBGTAGPTB3VS24W.SEARCH&ppt=hp&ppn=homepage&ssid=smh464qpmo0000001745288810546&qH=2f54b45b321e3ae5',
            'source': 'Flipkart'
        }
    ],
    'samsung s25': [
        {
            'title': 'Samsung Galaxy S25 5G (256GB) - Navy Blue',
            'price': 80999,
            'price_history': generate_price_history(80999, 0.07),
            'url': 'https://www.amazon.in/Samsung-Galaxy-Smartphone-Storage-Camera/dp/B0DSKNQ4YR/ref=sr_1_1_sspa?crid=2V71FUAJ68LO1&dib=eyJ2IjoiMSJ9.h3PDRucT_90IW8n6HrId2LrF6Xgy4UrQTZdD1DVyoldaWQI9AzH6q7zofQhbb210m0ggr5cwV1EVbdcnFlaguZsk1zDMQSIkmwXVyrx-VIF6IVOBLdkMtBg8wwlPv5ywsTdQ98sIPOR9ROByrm4-eNjoR5x0WytEgsYGdYgJN5FRR6pN2NvzV-sHeP9on02-UiSkwhmZgeNSPmH_IiUhWS0NJksu2uRIBSmncPThCcQ.9whawTUMXcexxLBkgh-xgOSBe9LWVw6f2wtk-su4LBg&dib_tag=se&keywords=s24&qid=1745289067&sprefix=s24%2Caps%2C281&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1',
            'source': 'Amazon'
        },
        {
            'title': 'SAMSUNG Galaxy S25 5G (Navy Blue, 256 GB)',
            'price': 80999,
            'price_history': generate_price_history(80999, 0.05),
            'url': 'https://www.flipkart.com/samsung-galaxy-s25-5g-navy-256-gb/p/itm277a7d1824e44?pid=MOBH8K8U4ZPHSNKK&lid=LSTMOBH8K8U4ZPHSNKKGKHZNG&marketplace=FLIPKART&q=s25+5g&store=tyy%2F4io&srno=s_1_7&otracker=AS_Query_OrganicAutoSuggest_3_3_na_na_ps&otracker1=AS_Query_OrganicAutoSuggest_3_3_na_na_ps&fm=search-autosuggest&iid=08c41b26-6f40-4df9-8add-9f02cc7337a1.MOBH8K8U4ZPHSNKK.SEARCH&ppt=sp&ppn=sp&ssid=u55pfbvf5c0000001745289150658&qH=7059ccee4d4092e0',
            'source':'Flipkart'
        }
    ],
    'macbook air': [
        {
            'title': 'Apple 2025 MacBook Air (13-inch, Apple M4 chip with 10-core CPU and 10-core GPU, 16GB Unified Memory, 512GB) ',
            'price': 119000,
            'price_history': generate_price_history(119000, 0.06),
            'url': 'https://www.amazon.in/Apple-MacBook-13-inch-10-core-Unified/dp/B0DZD8QJBH/ref=sr_1_3?crid=2K9QAAJWG2WPR&dib=eyJ2IjoiMSJ9.L2Hu7nsAw269fTBuFKBbdvT1Q0UdlXss5ACXd6svNbTV-Mbr7RLno_1gJSjWyCksItufqxEnACY4yy92t1vomj-5Et95lLnUK9CSYIEEg089-RToKRiqC1Fgp_leZrdEwl4BRRT6nJco2q2KLEd-AVfee2cM1mz2Jv2r3Cqdn6813G2FUlJLppfx5OzRJnfDalat17MLVAH9IFv027Z9KFR9ckUwioDQ5JYlgd6sNvU.DCEoJVU93ObuwTgPd6apCD78b-4eJBI7jTqaL0iGDWY&dib_tag=se&keywords=macbook%2Bair%2Bm4&qid=1745289296&sprefix=macb%2Caps%2C277&sr=8-3&th=1',
            'source': 'Amazon'
        },
        {
            'title': 'Apple MacBook Air Apple M4 - (16 GB/256 GB SSD/macOS Sequoia) MW1L3HN/A  (15.3 inch, Midnight, 1.51 Kg)',
            'price': 124000,
            'price_history': generate_price_history(124000, 0.05),
            'url': 'https://www.flipkart.com/apple-macbook-air-m4-16-gb-256-gb-ssd-macos-sequoia-mw1l3hn-a/p/itmb9ec5b746c763?pid=COMH9ZWQMCME2ZEN&lid=LSTCOMH9ZWQMCME2ZENK6V3N1&marketplace=FLIPKART&q=macbook+air+m4&store=6bo%2Fb5g&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&fm=search-autosuggest&iid=9ba33734-3600-4eb1-9194-1e724f807ae5.COMH9ZWQMCME2ZEN.SEARCH&ppt=sp&ppn=sp&ssid=eptznfh9jk0000001745289287612&qH=a3dc101ea3bce06d',
            'source': 'Flipkart'
        }
    ],
    'nothing phone 3a pro': [
        {
            'title': 'Nothing Phone (3a) Pro 5G (Black, 8GB RAM + 256GB Storage',
            'price': 30360,
            'price_history': generate_price_history(30360, 0.05),
            'url': 'https://www.amazon.in/Nothing-Phone-Black-256GB-Storage/dp/B0DZTQ44FC/ref=sr_1_4?crid=S8GXQTWTDTBG&dib=eyJ2IjoiMSJ9.xPMcvwY3UBJq868QxVIETH3_2BhnzVS3b9NMmFUTf_u4yJ2uI2aRr1Y0sQIiuNkU_Ltn7PWsrSOXcw2OrwfbSqUpgxix24ywU_JVYdt1WkDANMfwt8H_ZSwzeVnxHwzhSygSp32RuidDOlGe5fu2_nk_DeMIh3pv9mHdjnAKsk65wEhw97CBjFPDmQXmmJ4RQPw0stY1uE78ijUzc-juEe1aON72oLRHnyaTN54K74E.v76L3Cs70XRHdwZHVWfsqchx3LZewUsPe7p5tjLvcy4&dib_tag=se&keywords=nothing+phone+3a+pro&qid=1745290070&sprefix=nothing+phone+3a+%2Caps%2C300&sr=8-4',
            'source': 'Amazon'
        },
        {
            'title': 'Nothing Phone (3a) Pro 5G (Black, 8GB RAM + 256GB Storage',
            'price': 31999,
            'price_history': generate_price_history(31999, 0.05),
            'url': 'https://www.flipkart.com/nothing-phone-3a-pro-black-256-gb/p/itm04daaef6652d4?pid=MOBH8G3PGBUAQDJ7&lid=LSTMOBH8G3PGBUAQDJ7MTNYQQ&marketplace=FLIPKART&q=nothing%20phone%203a%20pro&sattr[]=color&sattr[]=storage&sattr[]=ram&st=ram',
            'source': 'Flipkart'
        }
    ],
    'apple watch series 10': [
        {
            'title': 'Apple Watch Series 10 [GPS 42 mm] Smartwatch with Jet Black Aluminium Case with Black Sport Band - S/M. Fitness Tracker, ECG App, Always-On Retina Display, Water Resistant',
            'price': 46900,
            'price_history': generate_price_history(46900, 0.05),
            'url': 'https://www.amazon.in/Apple-Watch-Smartwatch-Aluminium-Always/dp/B0DGJ6MH27/ref=sr_1_1_sspa?crid=RU99ADS25511&dib=eyJ2IjoiMSJ9.EjG2Lw_eKX38szXCnux5CCRiHfNpAFMX87zY9fPdHFbjaEV0PYwTauLg9jNjNjX8gm98DTWMLblkexXZdyNM-kL7Pm8H48o7IEzOBPo9_wur0EvoW5b3K49fwSUSx0RHi1B2r1IYCdteHyyINl5nIsHoqwHNux0vRubHA1t_JNR8t29vQJkYprhUWpL7EeYJaETxzW7GxANKphs8ucZ0G_SyK8ABT_atXVbuIpH28Ts.rWbKfsbaNYVXbDzjePjye5SEu9y5T1tK4M0cOoO54ro&dib_tag=se&keywords=apple%2Bwatch%2Bseries%2B10&nsdOptOutParam=true&qid=1745290667&sprefix=apple%2B%2Caps%2C280&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1',
            'source': 'Amazon'
        },
        {
            'title': 'Apple Watch Series 10 [GPS 42 mm] Smartwatch with Jet Black Aluminium Case with Black Sport Band - S/M. Fitness Tracker, ECG App, Always-On Retina Display, Water Resistant',
            'price': 46900,
            'price_history': generate_price_history(46900, 0.05),
            'url': 'https://www.flipkart.com/apple-watch-series-10-gps-42mm-jet-black-aluminium-sport-band/p/itm186d892337bc4?pid=SMWH4JBWJHRCMMX8&lid=LSTSMWH4JBWJHRCMMX8EWZBQI&marketplace=FLIPKART&q=apple%20watch%20series%2010&sattr[]=color&sattr[]=display_size&st=display_size',
            'source': 'Flipkart'
        }
    ],
    # New Electronics Items
    'sony xm5': [
        {
            'title': 'Sony WH-1000XM5 Wireless Noise Cancelling Headphones, 30Hr Battery, 8 Mics for Clear Calling, Black',
            'price': 26990,
            'price_history': generate_price_history(26990, 0.05),
            'url': 'https://www.amazon.in/Sony-WH-1000XM5-Cancelling-Headphones-Battery/dp/B09Y2MHXT1',
            'source': 'Amazon'
        },
        {
            'title': 'Sony WH-1000XM5 Bluetooth Headset with Mic and Alexa Voice Control (Black, Over the Ear)',
            'price': 27990,
            'price_history': generate_price_history(27990, 0.05),
            'url': 'https://www.flipkart.com/sony-wh-1000xm5-bluetooth-headset-mic-alexa-voice-control/p/itm0d179592c1ceb',
            'source': 'Flipkart'
        }
    ],
    'samsung tv 55 inch': [
        {
            'title': 'Samsung 138 cm (55 inches) D Series Brighter Crystal 4K Vivid Pro Ultra HD Smart LED TV ',
            'price': 46990,
            'price_history': generate_price_history(47990, 0.05),
            'url': 'https://www.amazon.in/Samsung-inches-Crystal-Vivid-UA55DUE77AKLXL/dp/B0CX5FRD9H/ref=sr_1_1_sspa?crid=2G3DFBHNKZURB&dib=eyJ2IjoiMSJ9.po_xnI7AR-huvB5141KKjpIjoilwAjqfnTdJJCmTrzsggOOThjIPDkvAUuWE93FZYJGk3WZvxN0zuYCu_XOZkPm3av0x4OGYQ1L91B9RxjwhiF8Qbq_1lKdAU-7MBIrGmm70snjsj0Ui7ezn7T1EFFcaolK2eOryhnirYAWd7t34q_Nebtuo9JP1CjgIK0medsVduBIdBvFnP80J20aO1DRAm8qhTLqGOf65SdmPZwA._XRoX9KpfJiFLHbiK6jNh9n5iql_wTt3e24USnsqIFE&dib_tag=se&keywords=samsung%2Btv%2B55%2Binch&nsdOptOutParam=true&qid=1745296728&sprefix=samsung%2Btv%2B%2Caps%2C292&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1',
            'source': 'Amazon'
        },
        {
            'title': 'Samsung 138 cm (55 inches) D Series Brighter Crystal 4K Vivid Pro Ultra HD Smart LED TV ',
            'price': 45990,
            'price_history': generate_price_history(45990, 0.05),
            'url': 'https://www.flipkart.com/samsung-new-d-series-brighter-crystal-4k-vision-pro-2024-edition-138-cm-55-inch-ultra-hd-4k-led-smart-tizen-tv-upscaling-multiple-voice-assistance-remote-purcolor-hdr-10-auto-game-mode-q-symphony-knox-security/p/itm8580c5c3990d8?pid=TVSGYWKBJHNSRN9N&lid=LSTTVSGYWKBJHNSRN9NMQXR3A&marketplace=FLIPKART&q=samsung+tv+55+inch&store=ckf%2Fczl&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&fm=search-autosuggest&iid=3c49a921-67a0-47fc-a005-939ede04d82d.TVSGYWKBJHNSRN9N.SEARCH&ppt=pp&ppn=pp&ssid=q8ryc9q8nk0000001745296742655&qH=eca762701aeb8e64',
            'source': 'Flipkart'
        }
    ],
    # New Footwear Items
    'nike air max': [
        {
            'title': 'Nike Men\'s Air Max Impact 4 Basketball Shoes',
            'price': 7495,
            'price_history': generate_price_history(7495, 0.05),
            'url': 'https://www.amazon.in/Nike-Impact-Basketball-CZ5708-004-Black/dp/B0BDH5LBW3',
            'source': 'Amazon'
        },
        {
            'title': 'Nike AIR MAX IMPACT 4 Basketball Shoes For Men (Black)',
            'price': 7097,
            'price_history': generate_price_history(7097, 0.05),
            'url': 'https://www.flipkart.com/nike-air-max-impact-4-basketball-shoes-men/p/itm979c4ca36c5d4',
            'source': 'Flipkart'
        }
    ],
    'adidas ultraboost': [
        {
            'title': 'Adidas Men\'s Ultraboost 23 Running Shoes',
            'price': 11999,
            'price_history': generate_price_history(11999, 0.05),
            'url': 'https://www.amazon.in/adidas-Ultraboost-Running-Shoes-GZ3578/dp/B0BSN1X7QD',
            'source': 'Amazon'
        },
        {
            'title': 'ADIDAS Ultraboost 23 Running Shoes For Men (Grey)',
            'price': 10999,
            'price_history': generate_price_history(10999, 0.05),
            'url': 'https://www.flipkart.com/adidas-ultraboost-23-running-shoes-men/p/itmbdaa64e5e6efe',
            'source': 'Flipkart'
        }
    ],
    'puma softride': [
        {
            'title': 'Puma Unisex-Adult Softride Vital Clean Sneaker',
            'price': 3559,
            'price_history': generate_price_history(3559, 0.05),
            'url': 'https://www.amazon.in/Puma-Softride-Running-Shoes-383397/dp/B0C6ZFFPK6',
            'source': 'Amazon'
        },
        {
            'title': 'Puma Softride Vital Clean Running Shoes For Men (White)',
            'price': 3299,
            'price_history': generate_price_history(3299, 0.05),
            'url': 'https://www.flipkart.com/puma-softride-vital-clean-running-shoes-men/p/itm3ad65e77d7cad',
            'source': 'Flipkart'
        }
    ],
    # New Bags Items
    'american tourister': [
        {
            'title': 'American Tourister Ivy 69 cms Medium Check-in Polypropylene Hardsided 4 Wheeler Luggage/Suitcase/Trolley Bag',
            'price': 3699,
            'price_history': generate_price_history(3699, 0.05),
            'url': 'https://www.amazon.in/American-Tourister-Medium-Polypropylene-Hardsided/dp/B07VZJQFSD',
            'source': 'Amazon'
        },
        {
            'title': 'American Tourister Ivy 68 cm Medium Check-in Polypropylene Hardside 4 Wheeler Luggage Suitcase',
            'price': 3499,
            'price_history': generate_price_history(3499, 0.05),
            'url': 'https://www.flipkart.com/american-tourister-ivy-68-cm-medium-check-polypropylene-hardside-4-wheeler-luggage-suitcase/p/itm9dbf6f5df8ca2',
            'source': 'Flipkart'
        }
    ],
    'skybags backpack': [
        {
            'title': 'Skybags Bingo Plus 46 Cms Polyester Casual Backpack with Laptop Compartment',
            'price': 1249,
            'price_history': generate_price_history(1249, 0.05),
            'url': 'https://www.amazon.in/Skybags-Bingo-Plus-Polyester-Laptop/dp/B0B95Q7BY5',
            'source': 'Amazon'
        },
        {
            'title': 'Skybags Bingo Plus 32 L Backpack with Laptop Compartment',
            'price': 999,
            'price_history': generate_price_history(999, 0.05),
            'url': 'https://www.flipkart.com/skybags-bingo-plus-32-l-backpack-laptop-compartment/p/itm0a10bf2389232',
            'source': 'Flipkart'
        }
    ],
    'wildcraft duffle bag': [
        {
            'title': 'Wildcraft Voyager Polyester Duffle Bag 55 Ltr with Wheels',
            'price': 2999,
            'price_history': generate_price_history(2999, 0.05),
            'url': 'https://www.amazon.in/Wildcraft-Voyager-Duffle-Bag-Black/dp/B07JGDC8KW',
            'source': 'Amazon'
        },
        {
            'title': 'Wildcraft Voyager 22 inch/55 cm Travel Duffel Bag With Wheels',
            'price': 2799,
            'price_history': generate_price_history(2799, 0.05),
            'url': 'https://www.flipkart.com/wildcraft-voyager-22-inch-55-cm-travel-duffel-bag-wheels/p/itm7a2fac5c12ab4',
            'source': 'Flipkart'
        }
    ]
}

def find_matching_products(query):
    """Find products that match the search query"""
    query = query.lower()
    results = []
    
    # Search through our sample database
    for key, products in SAMPLE_PRODUCTS.items():
        if query in key or any(query in product['title'].lower() for product in products):
            # Create a copy of each product to avoid modifying the original database
            results.extend([product.copy() for product in products])
    
    # If no exact matches, try partial matches
    if not results:
        for key, products in SAMPLE_PRODUCTS.items():
            for word in query.split():
                if word in key or any(word in product['title'].lower() for product in products):
                    # Create a copy of each product to avoid modifying the original database
                    results.extend([product.copy() for product in products])
                    break
    
    # No price variations - keep exact prices as defined in SAMPLE_PRODUCTS
    
    return list({product['source']: product for product in results}.values())  # Remove duplicates

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare_prices():
    product_name = request.form.get('product_name')
    if not product_name:
        return jsonify({'error': 'Product name is required'})

    logger.info(f"Comparing prices for: {product_name}")
    
    # Simulate network delay
    time.sleep(random.uniform(0.5, 1.5))
    
    # Get matching products
    results = find_matching_products(product_name)
    
    logger.info(f"Found {len(results)} results")
    return jsonify({'results': results})

@app.route('/price_history', methods=['GET'])
def get_price_history():
    product_id = request.args.get('product_id')
    source = request.args.get('source')
    
    # Debug logging
    logger.info(f"Price history request: product_id={product_id}, source={source}")
    
    if not product_id or not source:
        logger.error("Missing required parameters")
        return jsonify({'error': 'Product ID and source are required'})
    
    try:
        # First try exact match
        for key, products in SAMPLE_PRODUCTS.items():
            for product in products:
                # Decode the URL-encoded product_id for comparison
                decoded_product_id = urllib.parse.unquote(product_id)
                
                # Log comparison for debugging
                logger.info(f"Comparing: '{decoded_product_id}' with '{product['title']}', source: '{source}' with '{product['source']}'")
                
                # Check for exact match on title and source
                if product['title'] == decoded_product_id and product['source'].lower() == source.lower():
                    logger.info(f"Found exact match: {product['title']}")
                    return jsonify({'history': product['price_history']})
                    
        # If no exact match, try partial title match
        for key, products in SAMPLE_PRODUCTS.items():
            for product in products:
                decoded_product_id = urllib.parse.unquote(product_id)
                if (decoded_product_id.lower() in product['title'].lower() or 
                    product['title'].lower() in decoded_product_id.lower()) and \
                   product['source'].lower() == source.lower():
                    logger.info(f"Found partial match: {product['title']}")
                    return jsonify({'history': product['price_history']})
        
        # If still not found, try just matching source and return a random product
        # This is a fallback to ensure we always show something
        for key, products in SAMPLE_PRODUCTS.items():
            for product in products:
                if product['source'].lower() == source.lower():
                    logger.info(f"Fallback match by source: {product['title']}")
                    # Use dummy data if needed
                    dummy_data = [
                        {"date": "2023-12-01", "price": product['price'] * 1.1},
                        {"date": "2024-01-01", "price": product['price'] * 1.05},
                        {"date": "2024-02-01", "price": product['price'] * 0.95},
                        {"date": "2024-03-01", "price": product['price'] * 1.0},
                        {"date": "2024-04-01", "price": product['price'] * 0.98},
                        {"date": "2024-05-01", "price": product['price']}
                    ]
                    return jsonify({'history': product.get('price_history', dummy_data)})
        
        logger.error(f"No match found for product_id={product_id}, source={source}")
        return jsonify({'error': 'Product not found'})
    
    except Exception as e:
        logger.error(f"Error in price_history: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True) 