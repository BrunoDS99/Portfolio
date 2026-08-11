from scrape import scrape_cafes_from_osm

# Test with New York
print("Testing New York...")
cafes = scrape_cafes_from_osm("New York, NY", radius=3000, max_results=10)

print(f"\nFound {len(cafes)} cafes:")
for cafe in cafes[:5]:
    print(f"  - {cafe['name']}")
    print(f"    Location: {cafe['location']}")
    print(f"    WiFi: {cafe['has_wifi']}")
    print()