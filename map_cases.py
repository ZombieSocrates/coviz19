import folium
import pandas as pd 
import pathlib
import requests

from covid_data import current_tests_by_state

HTML_OUT = pathlib.Path.home() / "Desktop"
STATES_GEOJSON_URL = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json"
# Files downloaded from sketchy sources - world population review.com
STATE_POP_FILE = HTML_OUT / "US_POP.csv"
STATE_ABBREV_FILE = HTML_OUT / "US_ABBREVS.csv"


def get_state_geometries():
    '''move out of here after basic maps are done'''
    geo_rsp = requests.get(STATES_GEOJSON_URL)
    return geo_rsp.json()


def get_population_totals():
    '''move out of here after basic maps are done'''
    state_pops = pd.read_csv(STATE_POP_FILE)
    state_abbrevs = pd.read_csv(STATE_ABBREV_FILE)
    merged = state_pops.merge(state_abbrevs, on = "State")
    merged.drop(labels = ["State","rank","Abbrev"], axis = 1, inplace = True)
    return merged.rename(columns = {"Code":"state"})


def handle_colname(map_column, method = "filename"):
    name_map = {
        "positive": {
            "legend": "Positive COVID-19 Tests",
            "filename": "test_positive" 
        },
        "total": {
            "legend": "Total COVID-19 Tests",
            "filename": "test_total"
        },
        "positive_rate": {
            "legend": "Positive Test Rate",
            "filename": "test_pos_pct"
        },
        "positive_per_1e5": {
            "legend": "Positive Tests per 100,000",
            "filename": "pos_per_1e5"
        },
        "total_per_1e5": {
            "legend": "Total Tests per 100,000",
            "filename": "test_per_1e5"
        }
    }
    return name_map[map_column][method]


def make_choropleth(data_df, map_column, 
        shape_object = get_state_geometries()
        ):
    '''https://python-graph-gallery.com/292-choropleth-map-with-folium/'''
    m = folium.Map(location=[37, -102], zoom_start=5)
    choro_cols = ["state", map_column]
    m.choropleth(geo_data=shape_object,
        name="choropleth",
        data=data_df,
        columns=choro_cols,
        key_on="feature.id",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=handle_colname(map_column, "legend")
        )
    folium.LayerControl().add_to(m)
    save_as = HTML_OUT / f"{handle_colname(map_column, 'filename')}.html"
    print(f"Saving {save_as}...")
    m.save(str(save_as))


def main():
    testing_df = current_tests_by_state()
    testing_df["positive_rate"] = testing_df["positive"] / testing_df["total"]
    
    popu_df = get_population_totals()
    testing_df = testing_df.merge(popu_df, how = "inner", on = "state") #how = left
    testing_df["positive_per_1e5"] = testing_df["positive"] * 1e5 / testing_df["Pop"]
    testing_df["total_per_1e5"] = testing_df["total"] * 1e5 / testing_df["Pop"]

    geoms = get_state_geometries()
    for colname in ["positive","positive_rate","total", "positive_per_1e5", "total_per_1e5"]:
        make_choropleth(data_df = testing_df, 
            map_column = colname,
            shape_object = geoms
            )


if __name__ == "__main__":
    main()
    # import ipdb
    # ipdb.set_trace()
