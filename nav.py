import folium
import requests
import json

def get_route(origin, destination, api_key):
    """Retrieve route coordinates from GraphHopper API."""
    base_url = "https://graphhopper.com/api/1/route"
    params = {
        "point": f"{origin[1]},{origin[0]}|{destination[1]},{destination[0]}",  # Note: GraphHopper expects Lon,Lat
        "key": api_key,
        "vehicle": "car",
        "locale": "en",
        "points_encoded": "false",
        "type": "json",
        "elevation": "false",
        "point_hint": "0;0",
        "ch.disable": "true",
        "calc_points": "true",
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
    except Exception as err:
        print(f"Other Error: {err}")
    else:
        try:
            return response.json()
        except json.JSONDecodeError as json_err:
            print(f"JSON Decode Error: {json_err}")
            print("Response Text:")
            print(response.text)  # This might give a clue about the error
            return None

def plot_route_on_map(route_data, origin, destination):
    """Plot the route on a Folium map."""
    if route_data is None:
        return
    
    # Extract route path
    try:
        route_path = [(step[1], step[0]) for step in route_data['paths'][0]['points']['coordinates']]  # Note: Folium expects Lat,Lon
    except KeyError as key_err:
        print(f"Key Error: {key_err}. Check if 'paths' or 'coordinates' exist in the response.")
        print("Route Data:")
        print(json.dumps(route_data, indent=4))  # This will show you the actual response
        return
    
    # Create Map
    m = folium.Map(location=[(origin[0] + destination[0])/2, (origin[1] + destination[1])/2], zoom_start=10)
    
    # Add origin and destination markers
    folium.Marker([origin[0], origin[1]], popup="Origin").add_to(m)
    folium.Marker([destination[0], destination[1]], popup="Destination").add_to(m)
    
    # Plot the route
    folium.PolyLine(route_path, color='blue', weight=2.5, opacity=1).add_to(m)
    
    # Save the map as an HTML file
    m.save('route_map.html')
    print("Map saved as route_map.html")

if __name__ == "__main__":
    # Your GraphHopper API Key
    api_key = "YOUR_GRAPHHOPPER_API_KEY_HERE"
    
    # Define origin and destination (Latitude, Longitude)
    origin = (40.7128, -74.0060)  # New York City
    destination = (34.0522, -118.2437)  # Los Angeles
    
    route_data = get_route(origin, destination, api_key)
    plot_route_on_map(route_data, origin, destination)
