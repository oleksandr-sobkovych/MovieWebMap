"""Build the web map."""


import folium


def setup():
    """Create a new feature group.

    :return: FeatureGroup object
    """
    fg = folium.FeatureGroup(name="Movie map")

    return fg


def add_marker(fg: folium.FeatureGroup(), place: tuple, tooltip: str, data: dict):
    """Add a marker to a feature group.

    :param fg: feature group
    :param place: a tuple of location information
    :param tooltip: what to display on hover
    :param data: a dictionary with all necessary info
    """
    adder = "     &     ".join(data[place[2]]["place"][place[0]]["name"].keys())
    fg.add_child(folium.Marker((place[1].latitude, place[1].longitude),
                               popup="<i>{}</i>".format(adder),
                               tooltip=tooltip))


def map_constr(fg: folium.FeatureGroup(), loc: tuple, name: str = "map.html"):
    """Construct the layered map.

    :param fg: external feature group
    :param loc: location of the user
    :param name: html file name
    :return: None
    """
    m = folium.Map(location=loc, zoom_start=2)
    fg.add_child(folium.Marker(
        location=loc,
        popup='Your location',
        icon=folium.Icon(color='red')
    ))

    new_feat = folium.FeatureGroup(name="World Part")
    new_feat.add_child(folium.GeoJson(data=open("world.json", encoding="utf-8-sig").read(),
                                      style_function=lambda x: {'fillColor': 'green'
                                                                if x["properties"]["REGION"] < 3
                                                                else "blue" if 3 <= x["properties"]["REGION"] < 5
                                                                else "orange" if 5 <= x["properties"]["REGION"] < 10
                                                                else "red"}))
    folium.LatLngPopup().add_to(m)
    m.add_child(fg)
    m.add_child(new_feat)
    m.add_child(folium.LayerControl())
    m.save(name)
