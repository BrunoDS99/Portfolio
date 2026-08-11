from flask import Flask, render_template, request
from scrape import scrape_cafes_from_osm, geocode_location

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', 
                          cafes=[], 
                          map_center=None, 
                          location=None)

@app.route('/search')
def search():
    location = request.args.get('location', '')
    radius = int(request.args.get('radius', 5000))
    max_results = int(request.args.get('max_results', 24))
    
    if not location:
        return render_template('index.html', 
                              cafes=[], 
                              map_center=None, 
                              location=None,
                              error='Please enter a location.')
    
    # Get cafes from OpenStreetMap
    cafes = scrape_cafes_from_osm(location, radius, max_results)
    
    # Geocode location for map center
    coords = geocode_location(location)
    map_center = {'lat': coords[0], 'lng': coords[1]} if coords else None
    
    return render_template('index.html', 
                          cafes=cafes, 
                          location=location,
                          map_center=map_center)

@app.route('/api/cafes')
def api_cafes():
    location = request.args.get('location', '')
    radius = int(request.args.get('radius', 5000))
    max_results = int(request.args.get('max_results', 24))
    
    if not location:
        return {'error': 'Location required'}, 400
    
    cafes = scrape_cafes_from_osm(location, radius, max_results)
    return {'cafes': cafes}

if __name__ == '__main__':
    app.run(debug=True)