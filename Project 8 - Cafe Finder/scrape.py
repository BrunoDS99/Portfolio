import requests
import time

def geocode_location(location):
    """Convert location name to coordinates"""
    try:
        # Check if already coordinates
        if ',' in location:
            parts = location.split(',')
            if len(parts) == 2:
                try:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    return (lat, lon)
                except:
                    pass
        
        url = "https://nominatim.openstreetmap.org/search"
        params = {'q': location, 'format': 'json', 'limit': 1}
        headers = {'User-Agent': 'CafeFinderApp/1.0'}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return (float(data[0]['lat']), float(data[0]['lon']))
        return None
    except:
        return None

def scrape_cafes_from_osm(location, radius=5000, max_results=24):
    """Scrape cafes from OpenStreetMap"""
    try:
        coords = geocode_location(location)
        if not coords:
            return []
        
        lat, lon = coords
        
        query = f"""
        [out:json];
        (
          node["amenity"="cafe"](around:{radius},{lat},{lon});
          node["shop"="coffee"](around:{radius},{lat},{lon});
        );
        out center {max_results};
        """
        
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query,
            headers={'User-Agent': 'CafeFinderApp/1.0'},
            timeout=30
        )
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        cafes = []
        
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            name = tags.get('name', '')
            
            if not name:
                continue
            
            if 'lat' in element and 'lon' in element:
                lat_c = element['lat']
                lon_c = element['lon']
            elif 'center' in element:
                lat_c = element['center']['lat']
                lon_c = element['center']['lon']
            else:
                continue
            
            cafes.append({
                'name': name,
                'location': tags.get('addr:city', '') or tags.get('addr:town', '') or location,
                'lat': lat_c,
                'lon': lon_c,
                'map_url': f"https://www.openstreetmap.org/?mlat={lat_c}&mlon={lon_c}&zoom=15",
                'has_wifi': tags.get('internet_access') == 'wlan' or tags.get('wifi') == 'yes',
                'has_sockets': tags.get('socket') == 'yes' or tags.get('outlet') == 'yes',
                'has_toilet': tags.get('toilets') == 'yes',
                'can_take_calls': tags.get('phone') is not None,
                'seats': tags.get('seats', ''),
                'coffee_price': '',
                'img_url': ''
            })
        
        # Remove duplicates
        seen = set()
        unique = []
        for cafe in cafes:
            if cafe['name'] not in seen:
                seen.add(cafe['name'])
                unique.append(cafe)
        
        return unique[:max_results]
        
    except Exception as e:
        print(f"Error: {e}")
        return []