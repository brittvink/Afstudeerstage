#!/usr/bin/env python

"""
File:         get_interesting_topics_in_cleaned_data.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is used to read a text file and put the data in a MySQL Database

The data is given with the input argument (-i).
The data is readed and put in the database
"""

import pandas as pd
import os

"""With this script dataframes are made with a selection of RSS feeds"""

outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'sentiment')
if not os.path.exists(outdir):
    os.makedirs(outdir)

df = pd.read_pickle("pre_processing/df_preprocessed.pkl")

topics_sentiment_food_list = [  "https://www.sciencedaily.com/rss/health_medicine/nutrition.xml",
                                "https://www.sciencedaily.com/rss/mind_brain/consumer_behavior.xml",
                                "https://www.sciencedaily.com/rss/plants_animals/agriculture_and_food.xml",
                                "https://www.sciencedaily.com/rss/plants_animals/food.xml",
                                "https://www.sciencedaily.com/rss/plants_animals/food_and_agriculture.xml",
                              ]

df_sentiment_food = df.loc[df['rss'].isin(topics_sentiment_food_list)]
df_sentiment_food.to_pickle(os.path.join(outdir,"df_sentiment_food.pkl"))


topics_sentiment_energy_list = ["https://www.sciencedaily.com/rss/matter_energy/energy_and_resources.xml",
                                "https://www.sciencedaily.com/rss/matter_energy/energy_policy.xml",
                                "https://www.sciencedaily.com/rss/matter_energy/nuclear_energy.xml",
                                "https://www.sciencedaily.com/rss/matter_energy/alternative_fuels.xml",
                                "https://www.sciencedaily.com/rss/earth_climate/renewable_energy.xml",
                                "https://www.sciencedaily.com/rss/science_society/energy_issues.xml",
                                "https://www.sciencedaily.com/rss/matter_energy/fossil_fuels.xml",
                                "https://www.sciencedaily.com/rss/strange_offbeat/fossils_ruins.xml"]

df_sentiment_energy = df.loc[df['rss'].isin(topics_sentiment_energy_list)]
df_sentiment_energy.to_pickle(os.path.join(outdir,"df_sentiment_energy.pkl"))


topics_kcbbe_list = ["https://www.sciencedaily.com/rss/space_time/solar_system.xml",
                "https://www.sciencedaily.com/rss/matter_energy/energy_and_resources.xml",
                "https://www.sciencedaily.com/rss/matter_energy/biochemistry.xml",
                "https://www.sciencedaily.com/rss/matter_energy/inorganic_chemistry.xml",
                "https://www.sciencedaily.com/rss/matter_energy/organic_chemistry.xml",
                "https://www.sciencedaily.com/rss/matter_energy/chemistry.xml",
                "https://www.sciencedaily.com/rss/matter_energy/electricity.xml",
                "https://www.sciencedaily.com/rss/matter_energy/energy_policy.xml"
                "https://www.sciencedaily.com/rss/matter_energy/wind_energy.xml",
                "https://www.sciencedaily.com/rss/matter_energy/batteries.xml",
                "https://www.sciencedaily.com/rss/matter_energy/nuclear_energy.xml",
                "https://www.sciencedaily.com/rss/matter_energy/fuel_cells.xml",
                "https://www.sciencedaily.com/rss/matter_energy/energy_technology.xml",
                "https://www.sciencedaily.com/rss/matter_energy/alternative_fuels.xml",
                "https://www.sciencedaily.com/rss/matter_energy/fossil_fuels.xml",
                "https://www.sciencedaily.com/rss/matter_energy/solar_energy.xml",
                "https://www.sciencedaily.com/rss/matter_energy/civil_engineering.xml",
                "https://www.sciencedaily.com/rss/matter_energy/forensics.xml",
                "https://www.sciencedaily.com/rss/matter_energy/engineering.xml",
                "https://www.sciencedaily.com/rss/matter_energy/materials_science.xml",
                "https://www.sciencedaily.com/rss/matter_energy/quantum_computing.xml",
                "https://www.sciencedaily.com/rss/computers_math/computational_biology.xml",
                "https://www.sciencedaily.com/rss/computers_math/computer_modeling.xml",
                "https://www.sciencedaily.com/rss/computers_math/computer_science.xml",
                "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
                "https://www.sciencedaily.com/rss/computers_math/computer_programming.xml",
                "https://www.sciencedaily.com/rss/computers_math/information_technology.xml",
                "https://www.sciencedaily.com/rss/plants_animals/genetically_modified.xml",
                "https://www.sciencedaily.com/rss/plants_animals/pests_and_parasites.xml",
                "https://www.sciencedaily.com/rss/plants_animals/cloning.xml",
                "https://www.sciencedaily.com/rss/plants_animals/drought.xml",
                "https://www.sciencedaily.com/rss/plants_animals/soil_types.xml",
                "https://www.sciencedaily.com/rss/plants_animals/bird_flu.xml",
                "https://www.sciencedaily.com/rss/plants_animals/agriculture_and_food.xml",
                "https://www.sciencedaily.com/rss/plants_animals/food.xml",
                "https://www.sciencedaily.com/rss/plants_animals/organic.xml",
                "https://www.sciencedaily.com/rss/plants_animals/biotechnology_and_bioengineering.xml",
                "https://www.sciencedaily.com/rss/plants_animals/food_and_agriculture.xml",
                "https://www.sciencedaily.com/rss/plants_animals/life_sciences.xml",
                "https://www.sciencedaily.com/rss/plants_animals/biochemistry.xml",
                "https://www.sciencedaily.com/rss/plants_animals/biotechnology.xml",
                "https://www.sciencedaily.com/rss/plants_animals/cell_biology.xml",
                "https://www.sciencedaily.com/rss/plants_animals/microbes_and_more.xml",
                "https://www.sciencedaily.com/rss/plants_animals/microbiology.xml",
                "https://www.sciencedaily.com/rss/plants_animals/viruses.xml",
                "https://www.sciencedaily.com/rss/plants_animals/bacteria.xml",
                "https://www.sciencedaily.com/rss/plants_animals/fungus.xml",
                "https://www.sciencedaily.com/rss/plants_animals/prions.xml",
                "https://www.sciencedaily.com/rss/earth_climate/renewable_energy.xml",
                "https://www.sciencedaily.com/rss/earth_climate/geoengineering.xml",
                "https://www.sciencedaily.com/rss/earth_climate/recycling_and_waste.xml",
                "https://www.sciencedaily.com/rss/earth_climate/mining.xml",
                "https://www.sciencedaily.com/rss/earth_climate/climate.xml",
                "https://www.sciencedaily.com/rss/earth_climate/earth_science.xml",
                "https://www.sciencedaily.com/rss/earth_climate/chemistry.xml",
                "https://www.sciencedaily.com/rss/earth_climate/environmental_awareness.xml",
                "https://www.sciencedaily.com/rss/earth_climate/drought.xml",
                "https://www.sciencedaily.com/rss/earth_climate/air_pollution.xml",
                "https://www.sciencedaily.com/rss/earth_climate/environmental_policy.xml",
                "https://www.sciencedaily.com/rss/earth_climate/oil_spills.xml",
                "https://www.sciencedaily.com/rss/earth_climate/acid_rain.xml",
                "https://www.sciencedaily.com/rss/earth_climate/global_warming.xml",
                "https://www.sciencedaily.com/rss/earth_climate/ozone_holes.xml",
                "https://www.sciencedaily.com/rss/earth_climate/pollution.xml",
                "https://www.sciencedaily.com/rss/earth_climate/hazardous_waste.xml",
                "https://www.sciencedaily.com/rss/earth_climate/air_quality.xml",
                "https://www.sciencedaily.com/rss/earth_climate/environmental_issues.xml",
                "https://www.sciencedaily.com/rss/earth_climate/sustainability.xml",
                "https://www.sciencedaily.com/rss/earth_climate/energy.xml",
                "https://www.sciencedaily.com/rss/earth_climate/ecology.xml",
                "https://www.sciencedaily.com/rss/earth_climate/water.xml",
                "https://www.sciencedaily.com/rss/earth_climate/coral_reefs.xml",
                "https://www.sciencedaily.com/rss/earth_climate/rainforests.xml",
                "https://www.sciencedaily.com/rss/earth_climate/wildfires.xml",
                "https://www.sciencedaily.com/rss/earth_climate/ecosystems.xml",
                "https://www.sciencedaily.com/rss/earth_climate/environmental_science.xml",
                "https://www.sciencedaily.com/rss/earth_climate/biodiversity.xml",
                "https://www.sciencedaily.com/rss/earth_climate/near-earth_object_impacts.xml",
                "https://www.sciencedaily.com/rss/science_society/energy_issues.xml",
                "https://www.sciencedaily.com/rss/science_society/ocean_policy.xml",
                "https://www.sciencedaily.com/rss/science_society/resource_shortage.xml",
                "https://www.sciencedaily.com/rss/science_society/bioethics.xml",
                "https://www.sciencedaily.com/rss/science_society/disaster_plan.xml",
                "https://www.sciencedaily.com/rss/science_society/political_science.xml",
                "https://www.sciencedaily.com/rss/matter_energy/energy_and_resources.xml",
                "https://www.sciencedaily.com/rss/strange_offbeat/matter_energy.xml",
                "https://www.sciencedaily.com/rss/strange_offbeat/earth_climate.xml",
                "https://www.sciencedaily.com/rss/strange_offbeat/fossils_ruins.xml"]

df_topics_kcbbe = df.loc[df['rss'].isin(topics_kcbbe_list)]
df_topics_kcbbe.to_pickle(os.path.join(outdir,"df_topics_kcbbe.pkl"))