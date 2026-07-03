import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
host = "localhost"
port = "5432"  # Default port for PostgreSQL
database = "International_debt_analysis"
username = "postgres"
password = "lavi" 
connection=f"postgresql://postgres:lavi@localhost:5432/{database}"
engine = create_engine(connection)
st.title("International Debt Analysis System")
st.header("Live SQL Business Analytics Engine")
st.subheader("select and execute any 30 verification queries to audit record from your table")
queries = {
    "Retrieve all distinct country names from the dataset.":
        'select distinct "Country Name" from all_country_metadata',

    "Count the total number of countries available":
       'select count("Country Name") from all_country_metadata',

    "Find the total number of indicators present":
        'select count("Indicator Name") from series_metadata',

        "Display the first 10 records of the dataset":
            'select * from all_country_metadata limit 10',
      "Calculate the total global debt":
            'select sum("Value") from all_country_metadata',

       "List all unique indicator names":
         'select distinct "Indicator Name" from series_metadata',

            "Find the number of records for each country":
                'select "Country Name",count("Country Name") from all_country_metadata group by "Country Name"',

            "Display all records where debt is greater than 1 billion USD":
                'SELECT * FROM all_country_metadata WHERE "Value" > 1000000000',

            "Find the minimum, maximum, and average debt values":
            'SELECT min("Value"),max("Value"),avg("Value") FROM all_country_metadata',

            "Count total number of records in the dataset":
                'select count(*) from all_country_metadata',  

            "Find the total debt for each country":
             'select "Country Name",sum("Value") from all_country_metadata group by "Country Name"',

            "Display the top 10 countries with the highest total debt":
               'select "Country Name",sum("Value") from all_country_metadata group by "Country Name" order by sum("Value") desc limit 10',

            "Find the average debt per country":
              'select "Country Name",avg("Value") from all_country_metadata group by "Country Name"',

            "Calculate total debt for each indicator":
               'select sum(a."Value") from all_country_metadata a right join series_metadata s on s."Code"=a."Series Code" group by a."Series Code"',

            "Identify the indicator contributing the highest total debt":
               'select sum(a."Value") from all_country_metadata a right join series_metadata s on s."Code"=a."Series Code" group by a."Series Code" order by sum(a."Value") desc NULLS LAST ',

            "Find the country with the lowest total debt":
               'select sum(a."Value") from all_country_metadata a right join series_metadata s on s."Code"=a."Series Code" group by a."Series Code" order by sum(a."Value") NULLS LAST', 

            "Calculate total debt for each country and indicator combination":
                'select sum(a."Value") from all_country_metadata a right join series_metadata s on s."Code"=a."Series Code" group by a."Series Code" order by sum(a."Value") desc NULLS LAST ',
            "Count how many indicators each country has.":
               'select "Series Code",count("Series Code") as "Indicator count" from all_country_metadata group by "Series Code"',
            "Display countries whose total debt is above the global average":
                'SELECT "Country Name",SUM("Value") AS total_debt FROM all_country_metadata GROUP BY "Country Name" HAVING SUM("Value") > (SELECT AVG(country_total)FROM (SELECT SUM("Value") AS country_total FROM all_country_metadata GROUP BY "Country Name") AS avg_table)ORDER BY total_debt DESC',
            "Rank countries based on total debt (highest to lowest)":
                'SELECT "Country Name",SUM("Value") AS total_debt,RANK() OVER (ORDER BY SUM("Value") DESC) AS debt_rank FROM all_country_metadata GROUP BY "Country Name" ORDER BY debt_rank',

            
            "Find the top 5 indicators contributing most to global debt":
               'SELECT a."Series Code",s."Indicator Name",s."Topic",SUM(a."Value") AS total_global_debt FROM  all_country_metadata as a JOIN series_metadata AS s ON a."Series Code" = s."Code" GROUP BY a."Series Code",s."Indicator Name",s."Topic" ORDER BY total_global_debt DESC LIMIT 5',

            "Calculate percentage contribution of each country to total global debt":
                'SELECT "Country Name", SUM("Value") AS total_debt, ROUND(((SUM("Value") * 100.0) / (SELECT SUM("Value") FROM all_country_metadata))::NUMERIC, 2) AS percentage_contribution FROM all_country_metadata GROUP BY "Country Name" ORDER BY percentage_contribution DESC',

            "Identify the top 3 countries for each indicator based on debt":
                'SELECT * FROM (SELECT "Series Name", "Country Name", SUM("Value") AS total_debt, RANK() OVER (PARTITION BY "Series Name" ORDER BY SUM("Value") DESC) AS rnk FROM all_country_metadata GROUP BY "Series Name", "Country Name") AS ranked WHERE rnk <= 3 ORDER BY "Series Name", rnk',

            "Find the difference between maximum and minimum debt for each country":
                 'SELECT "Country Name", MAX("Value") AS max_debt, MIN("Value") AS min_debt, MAX("Value") - MIN("Value") AS debt_difference FROM all_country_metadata GROUP BY "Country Name" ORDER BY debt_difference DESC',

            "Create a view for the top 10 countries with highest debt":
                  'SELECT * FROM top_10_countries_debt',

            "Categorize countries into:High Debt,Medium Debt,Low Debt (based on thresholds)":
                'SELECT "Country Name",SUM("Value") AS total_debt,CASE WHEN SUM("Value") >= 1000000000 THEN '"High Debt"' WHEN SUM("Value") >= 100000000 THEN '"Medium Debt"' ELSE '"Low Debt"' END AS debt_category FROM all_country_metadata GROUP BY "Country Name" ORDER BY total_debt DESC',

            "Use window functions to calculate cumulative debt per country":
                'SELECT "Country Name", "Year", "Value", SUM("Value") OVER (PARTITION BY "Country Name" ORDER BY "Year" ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_debt FROM all_country_metadata ORDER BY "Country Name", "Year"',

            "Find indicators where average debt is higher than overall average debt":
                 'SELECT "Series Name", AVG("Value") AS avg_debt FROM all_country_metadata GROUP BY "Series Name" HAVING AVG("Value") > (SELECT AVG("Value") FROM all_country_metadata) ORDER BY avg_debt DESC',

            "Identify countries contributing more than 5% of global debt":
                 'SELECT "Country Name", SUM("Value") AS total_debt, ROUND(((SUM("Value") * 100.0) / (SELECT SUM("Value") FROM all_country_metadata))::NUMERIC, 2) AS percentage_contribution FROM all_country_metadata GROUP BY "Country Name" HAVING ((SUM("Value") * 100.0) / (SELECT SUM("Value") FROM all_country_metadata)) > 5 ORDER BY percentage_contribution DESC',

            "Find the most dominant indicator (highest contribution) for each country":
                'SELECT * FROM (SELECT "Country Name", "Series Name", SUM("Value") AS total_debt, RANK() OVER (PARTITION BY "Country Name" ORDER BY SUM("Value") DESC) AS rnk FROM all_country_metadata GROUP BY "Country Name", "Series Name") AS ranked WHERE rnk = 1 ORDER BY "Country Name"'    
                                

}

selected = st.selectbox(
    "Choose Query",
    list(queries.keys())
)

if st.button("Execute SQL Query"):

    query = queries[selected]

    # Show SQL Query
    st.subheader("SQL Query")
    st.code(query, language="sql")

    df = pd.read_sql_query(
        queries[selected],
        connection
    )

    st.dataframe(df, use_container_width=True,hide_index=True)
