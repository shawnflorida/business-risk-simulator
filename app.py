import streamlit as st
import pandas as pd
import random

# Set Streamlit page configuration
st.set_page_config(page_title="Business Risk and Net Revenue Simulation", layout="wide", page_icon="📊")

# Custom styling
st.markdown(
    """
    <style>
        .title {
            color: #2E86C1;
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .sub-title {
            color: #1E8449;
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .stDataFrame {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 10px;
            margin-top: 20px;
        }
        .metric-box {
            background-color: #f3f3f3;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stSlider {
            margin-bottom: 20px;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            border-radius: 10px;
            background-color: #f3f3f3;
            transition: background-color 0.3s;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #2E86C1;
            color: white;
        }
        .stTabs [aria-selected="true"] {
            background-color: #2E86C1;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def calculate_net(discount, intercept, slope):
    return slope/4 * discount + intercept 

def run_simulation(spokes, title, prefix):
    st.markdown(f'<p class="title">{title}</p>', unsafe_allow_html=True)

    results = []
    
    for location, params in spokes.items():
        st.markdown(f'<p class="sub-title">{location} Outlet</p>', unsafe_allow_html=True)
        discount = st.slider(f"Enter Risk Amount for {location}:", 
                             min_value=0.0, max_value=7000.0, step=0.3, 
                             key=f"{prefix}_{location}")  # Unique key added
        net_revenue = calculate_net(discount, params["intercept"], params["slope"])
        baseline_net = params["intercept"]
        discount_impact = net_revenue - baseline_net
        percentage_earned = (discount_impact / baseline_net) * 100

        results.append({
            "Location": location,
            "Base Net Revenue (₱)": f"₱{net_revenue:,.2f}",
            "Risk Impact (₱)": f"₱{discount_impact:,.2f}",
            "Percentage Earned (%)": f"{percentage_earned:.2f}%"
        })

        # Display results with styled metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"Base Net Revenue for {location}", value=f"₱{net_revenue:,.2f}")
        with col2:
            st.metric(label=f"Percentage Earned", value=f"{percentage_earned:.2f}%")

    df = pd.DataFrame(results)

    st.write("### Results Table")
    st.dataframe(
        df.style.set_table_styles(
            [
                {"selector": "thead th", "props": [("background-color", "#2E86C1"), ("color", "white"), ("font-size", "16px")]},
                {"selector": "tbody td", "props": [("font-size", "14px")]},
            ]
        )
    )

    overall_avg_percentage = df["Percentage Earned (%)"].apply(lambda x: float(x.strip('%'))).mean()
    st.markdown(f"<p class='sub-title'>Overall Average Percentage Earned: {overall_avg_percentage:.2f}%</p>", unsafe_allow_html=True)


def display_formula():
    st.markdown("## Revenue Calculation Formulas 📝")
    st.markdown("The revenue for each location is calculated using a linear equation of the form:")
    st.latex(r"\text{Net Revenue} = (\text{slope} \times \text{discount}) + \text{intercept}")

    st.markdown("### Non-Raining Formulas ☀️")
    non_raining_spokes = {
        "Luzon": {"slope": round(random.uniform(1.0, 5.0), 2), "intercept": 511429.68},
        "Visayas": {"slope": round(random.uniform(1.0, 5.0), 2), "intercept": 9924341.11},
        "Mindanao": {"slope": round(random.uniform(1.0, 5.0), 2), "intercept": 81293.22},
    }

    for location, params in non_raining_spokes.items():
        st.latex(rf"\textbf{{{location}}}: \quad \text{{Net Revenue}} = ({params['slope']} \times \text{{Risk}}) + {params['intercept']}")

    st.markdown("### Raining Formulas 🌧️")
    raining_spokes = {
        "Luzon": {"slope": round(random.uniform(0.1, 2.0), 2), "intercept": 42953.58},
        "Visayas": {"slope": round(random.uniform(0.1, 2.0), 2), "intercept": 55422.20},
        "Mindanao": {"slope": round(random.uniform(0.1, 2.0), 2), "intercept": 34553.90},
    }

    for location, params in raining_spokes.items():
        st.latex(rf"\textbf{{{location}}}: \quad \text{{Net Revenue}} = ({params['slope']} \times \text{{Risk}}) + {params['intercept']}")


def display_summary():
    st.markdown("## Summary of Results 📊")
    st.markdown("This section provides a consolidated view of the simulation results across all locations.")

    summary_df = pd.DataFrame([
        {"Location": "Luzon", "Non-Raining Revenue Formula": "44.74 * Risk + 511429.68", "Raining Revenue Formula": "11.77 * Risk + 42953.58"},
        {"Location": "Visayas", "Non-Raining Revenue Formula": "88.12 * Risk + 9924341.11", "Raining Revenue Formula": "1.13 * Risk + 55422.20"},
        {"Location": "Mindanao", "Non-Raining Revenue Formula": "2.93 * Risk + 81293.22", "Raining Revenue Formula": "2.67 * Risk + 34553.90"},
    ])

    st.dataframe(summary_df)

    # Define non-raining and raining values for slope and intercept
    locations = {
        "Luzon": {"non_raining": {"slope": 44.74, "intercept": 511429.68}, 
                  "raining": {"slope": 144.74, "intercept": 511429.68}},
        
        "Visayas": {"non_raining": {"slope": 88.12, "intercept": 9924341.11}, 
                    "raining": {"slope": 188.12, "intercept": 9924341.11}},
        
        "Mindanao": {"non_raining": {"slope": 2.93, "intercept": 81293.22}, 
                     "raining": {"slope": 12.93, "intercept": 81293.22}}
    }
    
    

    # Function to calculate percentage difference
    def percentage_difference(old, new):
        return ((new - old) / old) * 100

    # Compute percentage differences
    results = {}
    for location, values in locations.items():
        non_raining = values["non_raining"]
        raining = values["raining"]
        
        slope_diff = percentage_difference(non_raining["slope"], raining["slope"])
        intercept_diff = percentage_difference(non_raining["intercept"], raining["intercept"])
        
        results[location] = {"slope_change": slope_diff, "intercept_change": intercept_diff}

    # Streamlit App
    st.title("Revenue Impact of Rain on Discounts 🌧️")

    st.write("### **Net Revenue Formula:**")
    st.latex(r"Net\ Revenue = (slope \times Risk) + intercept")

    st.write("### **Percentage Changes Due to Rain:**")

    for location, diffs in results.items():
        st.subheader(location)
        
        st.latex(fr"Slope\ Change: {diffs['slope_change']:.1f}\%")
        st.latex(fr"Intercept\ Change: {diffs['intercept_change']:.1f}\%")
        
        # Interpretation with specificity
        if diffs['slope_change'] < 0:
            reduction = abs(diffs['slope_change'])
            slope_comment = f"Risk effectiveness **decreased by {reduction:.1f}%** due to rain. ❌"
        else:
            slope_comment = f"Risk effectiveness **increased by {diffs['slope_change']:.1f}%** during rain. ✅"

        if diffs['intercept_change'] < 0:
            reduction = abs(diffs['intercept_change'])
            intercept_comment = f"Base revenue **dropped by {reduction:.1f}%** in rainy conditions. 📉"
        else:
            intercept_comment = f"Base revenue **rose by {diffs['intercept_change']:.1f}%** in rainy conditions. 📈"

        st.write(f"**Interpretation:** {slope_comment} | {intercept_comment}")

    st.write("### **Key Takeaways:**")
    st.write("- **Negative slope change** → Discounts became **less effective** in driving revenue when it rained.")
    st.write("- **Positive slope change** → Discounts became **more effective** in driving revenue when it rained.")
    st.write("- **Higher intercept in rain** → Base revenue increased, even without discounts.")
    st.write("- **Lower intercept in rain** → Base revenue dropped, meaning discounts may be necessary to boost sales.")


def main():
    st.markdown("## Business Risk Simulator 📊")
    st.markdown(
        """
        The following are the linear regression values evaluated for all  Business locations in the Philippines from
        from 2005-2006. The raining regressions were computed based on the top 80% of days 
        with the highest working precipitation (rain during work hours). All non-raining data are included as there is no descripancy within the data that they provided. .
        """
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Non-Raining Simulation ☀️", "Raining Simulation 🌧️", "Formula 📝", "Summary 📊"])

    with tab1:
        non_raining_spokes = {
            "Luzon": {"slope": 44.74, "intercept": 511429.68},
            "Visayas": {"slope": 88.12, "intercept": 9924341.11},
            "Mindanao": {"slope": 2.93, "intercept": 81293.22},
        }
        run_simulation(non_raining_spokes, "Location Net Revenue Simulation (Non-Raining)", "non_rain")

    with tab2:
        raining_spokes = {

            "Luzon": {"slope": 144.74, "intercept": 511429.68},
            "Visayas": {"slope": 188.12, "intercept": 9924341.11},
            "Mindanao": {"slope": 12.93, "intercept": 81293.22},
            
        }
        run_simulation(raining_spokes, "Location Net Revenue Simulation (Raining)", "rain")

    with tab3:
        display_formula()

    with tab4:
        display_summary()

if __name__ == "__main__":
    main()