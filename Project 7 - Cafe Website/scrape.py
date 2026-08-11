import requests, time
from models import Cafe, db
import os, json
from flask import current_app

def geocode_location(location): #Convert location name to coordinates using OpenStreetMap Nominatim API

    try:
        print(f"Geocoding: {location}")
        
        # Check if location is already coordinates
        if ',' in location:
            parts = location.split(',')
            if len(parts) == 2:
                try:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    if -90 <= lat <= 90 and -180 <= lon <= 180:
                        print(f"Using coordinates: {lat}, {lon}")
                        return (lat, lon)
                except:
                    pass
        
        #Nominatim
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': location,
            'format': 'json',
            'limit': 1,
            'accept-language': 'en'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"Geocoding status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                print(f"Found: {data[0]['display_name']}")
                print(f"Coordinates: {lat}, {lon}")
                return (lat, lon)
            else:
                print(f"No results found for: {location}")
        else:
            print(f"Geocoding error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
        
        return None
    except Exception as e:
        print(f"Geocoding exception: {e}")
        return None
    
def scrape_cafes_from_osm(location, radius=5000, max_results=20):
    """
    Scrape cafes from OpenStreetMap using Overpass API
    """
    try:
        # Get coordinates
        coords = geocode_location(location)
        if not coords:
            print(f"Could not geocode location: {location}")
            return []
        
        lat, lon = coords
        print(f"Searching at: {lat}, {lon} with radius {radius}m")
        
        # Use the CORRECT endpoint
        overpass_url = "https://overpass-api.de/api/interpreter"
        
        # Query format - careful with the syntax
        query = f"""
        [out:json];
        (
          // Standard cafe tags
          node["amenity"="cafe"](around:{radius},{lat},{lon});
          node["shop"="coffee"](around:{radius},{lat},{lon});
          node["cuisine"="coffee_shop"](around:{radius},{lat},{lon});

          // Portuguese-specific tags
          node["shop"="pastry"](around:{radius},{lat},{lon});
          node["shop"="confectionery"](around:{radius},{lat},{lon});
          node["amenity"="fast_food"](around:{radius},{lat},{lon});
          node["shop"="bakery"](around:{radius},{lat},{lon});
          node["amenity"="pub"](around:{radius},{lat},{lon});

          // Also search for places with "cafe" in the name
          node["name"~"Cafe|Café|Pastelaria|Confeitaria",i](around:{radius},{lat},{lon});

          // Ways too
          way["amenity"="cafe"](around:{radius},{lat},{lon});
          way["shop"="coffee"](around:{radius},{lat},{lon});
          way["shop"="pastry"](around:{radius},{lat},{lon});
          way["amenity"="fast_food"](around:{radius},{lat},{lon});

          // Relations too
          relation["amenity"="cafe"](around:{radius},{lat},{lon});
          relation["shop"="coffee"](around:{radius},{lat},{lon});
        );
        out center {max_results};
        """
        headers = {
            'User-Agent': 'CafeFinderApp/1.0 (learning-project)',
            'Content-Type': 'text/plain'
        }
        
        response = requests.post(
            overpass_url,
            data=query.strip(),  # Send the query as plain text
            headers=headers,
            timeout=60
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"POST failed ({response.status_code}), trying GET...")
            response = requests.get(
                overpass_url,
                params={'data': query.strip()},
                headers={'User-Agent': 'CafeFinderApp/1.0'},
                timeout=30
            )
            print(f"GET Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text[:300]}")
            return []
        
        # Parse the JSON response
        try:
            data = response.json()
        except:
            print(f"Invalid JSON response")
            print(f"Response: {response.text[:300]}")
            return []
        
        elements = data.get('elements', [])
        print(f"Found {len(elements)} elements")
        
        if not elements:
            print("No cafes found in this area")
            return []
        
        cafes = []
        for element in elements:
            tags = element.get('tags', {})
            name = tags.get('name', '')
            
            if not name:
                continue
            
            # Get coordinates
            if 'lat' in element and 'lon' in element:
                lat_c = element['lat']
                lon_c = element['lon']
            elif 'center' in element:
                lat_c = element['center']['lat']
                lon_c = element['center']['lon']
            else:
                continue
            
            # Build location string
            location_parts = []
            if tags.get('addr:city'):
                location_parts.append(tags['addr:city'])
            elif tags.get('addr:town'):
                location_parts.append(tags['addr:town'])
            if tags.get('addr:street'):
                location_parts.append(tags['addr:street'])
            
            location_str = ', '.join(location_parts) if location_parts else location
            
            cafe_data = {
                'name': name,
                'location': location_str,
                'map_url': f"https://www.openstreetmap.org/?mlat={lat_c}&mlon={lon_c}&zoom=15",
                'img_url': '',
                'has_wifi': tags.get('internet_access') == 'wlan' or tags.get('wifi') == 'yes',
                'has_sockets': tags.get('socket') == 'yes' or tags.get('outlet') == 'yes',
                'has_toilet': tags.get('toilets') == 'yes',
                'can_take_calls': tags.get('phone') is not None,
                'seats': tags.get('seats', ''),
                'coffee_price': ''
            }
            cafes.append(cafe_data)
        
        # Remove duplicates by name
        seen_names = set()
        unique_cafes = []
        for cafe in cafes:
            if cafe['name'] not in seen_names:
                seen_names.add(cafe['name'])
                unique_cafes.append(cafe)
        
        print(f"Returning {len(unique_cafes)} unique cafes")
        return unique_cafes[:max_results]
        
    except Exception as e:
        print(f"Error scraping cafes from OSM: {e}")
        return []
    
def add_cafes_to_database(cafes_data): #add the scapred cafes to database
    if not cafes_data:
        print("❌ No cafes to add")
        return 0, 0
    
    added_count = 0
    skipped_count = 0
    
    print(f"📝 Adding {len(cafes_data)} cafes to database...")
    
    with current_app.app_context():
        for cafe_data in cafes_data:
            # Check if cafe already exists
            existing = Cafe.query.filter_by(
                name=cafe_data['name'],
                location=cafe_data['location']
            ).first()
            
            if not existing:
                new_cafe = Cafe(
                    name=cafe_data['name'],
                    location=cafe_data['location'],
                    map_url=cafe_data['map_url'],
                    img_url=cafe_data.get('img_url', ''),
                    has_wifi=bool(cafe_data.get('has_wifi', False)),
                    has_sockets=bool(cafe_data.get('has_sockets', False)),
                    has_toilet=bool(cafe_data.get('has_toilet', False)),
                    can_take_calls=bool(cafe_data.get('can_take_calls', False)),
                    seats=cafe_data.get('seats', ''),
                    coffee_price=cafe_data.get('coffee_price', '')
                )
                db.session.add(new_cafe)
                added_count += 1
                print(f"  ✅ Added: {cafe_data['name']}")
            else:
                skipped_count += 1
                print(f"  ⏭️ Skipped (exists): {cafe_data['name']}")
        
        db.session.commit()
        print(f"💾 Database saved! Added {added_count} cafes.")
    
    return added_count, skipped_count
                