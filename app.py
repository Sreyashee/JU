

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend suitable for web apps

import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




@app.route("/api/plots")
def dashboard():
    df = pd.read_csv("Electric_Vehicle_Population_Data.csv")

    os.makedirs("static", exist_ok=True)

    # List to store the image paths and titles
    plot_data = []


    top_makes = df['Make'].value_counts().head(10)
    top_makes_data = [{"name": k, "value": int(v)} for k, v in top_makes.items()]
    plot_data.append({"title": "Top 10 EV Makes", "type": "combo", "data": top_makes_data, "description":"1. Displays the most popular EV models based on registration count.\n2. Analysis:\nBrands like Tesla, Nissan and Chevrolet dominate, indicating brand recognition and trust in EV technology.\nTesla leads due to its wide model variety and strong charging network.\n3. Key Features:\nBar graph ranking EV manufacturers.\nHoverable tooltips for make-specific insights", "position":"right"})

  
    
    top_models = df['Model'].value_counts().head(10)
    top_models_data = [{"name": k, "value": int(v)} for k, v in top_models.items()]
    plot_data.append({"title": "Top 10 EV Models", "type": "combo", "data": top_models_data, "description":"1. Displays the most popular EV models based on registration count.\n2. Analysis:\nModel Y, The Tesla Model 3 and Nissan Leaf are frequently at the top. These models balance price, performance, and range, explaining their popularity.\n3. Key Features:\nFocused comparison of specific models\nClear visualization of market-leading vehicles","position": "left" })



   # 3. EV Type Distribution (BAR + PIE)
    ev_type_counts = df['Electric Vehicle Type'].value_counts()
    ev_type_data = [{"name": k, "value": int(v)} for k, v in ev_type_counts.items()]
    plot_data.append({
        "title": "EV Type Distribution",
        "type": "combo",
        "data": ev_type_data, "description":"1. Categorizes registered EVs into types: Battery Electric Vehicles (BEVs), Plug-in Hybrids (PHEVs), etc.\n2. Analysis:\nBEVs usually make up the majority, suggesting a shift away from hybrids toward fully electric solutions.\n3. Key Features:\nYear-by-year registration tracking\nHighlights trends and consumer shifts\nUseful for predicting future growth", "position":"right"
    })


    model_year_counts = df['Model Year'].value_counts().sort_index()
    model_year_data = [{"name": str(k), "value": int(v)} for k, v in model_year_counts.items()]
    plot_data.append({"title": "EV Registrations by Model Year", "type": "combo", "data": model_year_data,"description":"1. Illustrates how many electric vehicles (EVs) were registered each year, showing the growth trend of EV adoptionuntil 2022. \n2. Analysis of the Graph\nA steady increase in registrations.\nFalling battery costs\nGovernment incentives and environmental policies\n3. Key Features:\nClear indication of peak registration years\nHelps identify momentum shifts in EV popularity","position": "left"})

    # 5. Distribution of Electric Range (HISTOGRAM — not for pie)
    range_series = df['Electric Range'].dropna()
    range_bins = pd.cut(range_series, bins=10)
    range_data = range_bins.value_counts().sort_index()
    range_chart_data = [{"name": str(interval), "value": int(count)} for interval, count in range_data.items()]
    plot_data.append({"title": "Distribution of Electric Range", "type": "combo", "data": range_chart_data,"description":"1. Displays how EVs are distributed based on their electric driving range.\n2. Analysis:\nMajority fall in the 100-300 mile range.\nIt shows how range anxiety is reducing with newer models offering more miles per charge.\n3.Key Features:\nInsight into battery capability growth\nHelps evaluate real-world usability of EVs", "position":"right"})

    # 6. EV Count by County (BAR + PIE)
    county_counts = df['County'].value_counts().head(10)
    county_data = [{"name": k, "value": int(v)} for k, v in county_counts.items()]
    plot_data.append({
        "title": "EV Count by County",
        "type": "combo",
        "data": county_data,"description":"1. Breaks down EV registrations by county within a state or region.\n2. Analysis:\nUrban counties typically show higher counts due to better infrastructure and awareness. Coastal and tech-heavy regions tend to lead.\n3. Key Features:\nGeo-distributed insights\nUseful for infrastructure planning\nHelps businesses target EV services geographically","position": "left"
    })

    # 7. EV Count by City (Top 10) (BAR + PIE)
    city_counts = df['City'].value_counts().head(10)
    city_data = [{"name": k, "value": int(v)} for k, v in city_counts.items()]
    plot_data.append({"title": "Top 10 Cities by EV Count", "type": "combo", "data": city_data,"description":"1. Highlights cities with the highest number of registered EVs\n2. Analysis:\nMajor cities like Seattle tops the list due to EV-friendly policies, dense populations, and better access to charging stations.\n3. Key Features:\nOffers city-specific focus\nSupports resource allocation and local campaigns", "position":"right"})


    # 8. EV Count by Electric Utility (BAR + PIE)
    utility_counts = df['Electric Utility'].value_counts().head(10)
    utility_data = [{"name": k, "value": int(v)} for k, v in utility_counts.items()]
    plot_data.append({
        "title": "EV Count by Electric Utility",
        "type": "combo",
        "data": utility_data,"description":"1. Shows the number of EVs associated with each electric utility provider.\n2. Analysis:\nLarger utilities serving urban areas show higher EV counts, indicating their readiness or challenges in managing increased demand.\n3. Key Features:\nBreakdown by energy provider\nUseful for grid planning and partnerships\nIdentifies utility zones with high EV penetration","position": "left"
    })

    # 9. CAFV Eligibility Distribution (BAR + PIE)
    cafv_counts = df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].value_counts()
    cafv_data = [{"name": k, "value": int(v)} for k, v in cafv_counts.items()]
    plot_data.append({
        "title": "CAFV Eligibility Distribution",
        "type": "combo",
        "data": cafv_data,"description":"1. Displays how many EVs qualify for Clean Alternative Fuel Vehicle (CAFV) incentives.\n2. Analysis:\nHigh eligibility rates indicate newer, more efficient models dominate. It also reflects successful implementation of clean vehicle standards.\n3. Key Features:\nHighlights incentive effectiveness\nCan drive policy and rebate analysis", "position":"right"
    })


    # Return the template with plot data
    # return render_template("dashboard.html", plot_data=plot_data)
    from flask import jsonify
    return jsonify(plot_data)

if __name__ == "__main__":
    app.run(debug=True)
