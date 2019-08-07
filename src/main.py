import config
import web

while True:
    print("traffic generator started...")
    print("----------------------------")
    print(f"clicking {config.click_depth} links deep into {len(config.root_urls)} different URL(s)")
    print(f"waiting between {config.min_wait} and {config.max_wait} seconds between requests")
    web.browse(config.root_urls)