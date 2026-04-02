from __future__ import annotations

import streamlit as st

from agents.graph import build_graph
from agents.state import RoomInput

st.set_page_config(page_title="DesignMate AI", layout="wide")
st.title("DesignMate AI — MVP")
st.caption("Autonomous interior design starter scaffold")

with st.sidebar:
    st.header("Room Inputs")
    room_type = st.selectbox("Room type", ["living_room", "bedroom", "office"])
    width_ft = st.number_input("Width (ft)", min_value=6.0, max_value=40.0, value=12.0)
    length_ft = st.number_input("Length (ft)", min_value=6.0, max_value=40.0, value=14.0)
    style = st.selectbox("Style", ["modern", "minimal", "scandinavian", "boho", "industrial"])
    budget = st.number_input("Budget ($)", min_value=200, max_value=10000, value=1500, step=100)
    colors = st.multiselect("Preferred colors", ["white", "black", "brown", "beige", "green", "blue", "gray"], default=["beige", "brown"])
    notes = st.text_area("Notes", placeholder="Need cozy seating, lots of light, renter-friendly...")
    uploaded = st.file_uploader("Room photo (optional for now)", type=["png", "jpg", "jpeg"])

    st.divider()
    st.header("Refinement Inputs")

    adjust_budget = st.checkbox("Adjust budget")
    if adjust_budget:
        budget = st.number_input("Revised budget ($)", min_value=200, max_value=10000, value=int(budget), step=100)

    avoid_colors = st.multiselect(
        "Avoid colors",
        ["white", "black", "brown", "beige", "green", "blue", "gray"],
    )
    must_have_categories = st.multiselect(
        "Must-have categories",
        ["sofa", "coffee_table", "rug", "floor_lamp", "bed", "nightstand", "desk", "desk_chair", "bookshelf"],
    )
    exclude_retailers = st.multiselect(
        "Exclude retailers",
        ["ikea", "amazon", "wayfair"],
    )
    refinement_notes = st.text_area(
        "Refinement notes",
        placeholder="e.g. Prefer items that ship fast, avoid anything too bulky...",
    )

    run = st.button("Generate design options", type="primary")

st.subheader("How this MVP maps to the proposal")
st.markdown(
    """
- **Perception**: stubbed room analysis for now
- **Planning**: LangGraph workflow with shared state
- **Product sourcing**: local mock catalog
- **Optimization**: simple scoring now, OR-Tools next checkpoint
- **Rendering**: placeholder summaries now, image generation later
"""
)

if run:
    request = RoomInput(
        room_type=room_type,
        width_ft=width_ft,
        length_ft=length_ft,
        style=style,
        budget=float(budget),
        colors=colors,
        notes=notes,
        image_path=uploaded.name if uploaded else None,
        avoid_colors=avoid_colors,
        exclude_retailers=exclude_retailers,
        must_have_categories=must_have_categories,
        refinement_notes=refinement_notes,
    )

    graph = build_graph()
    result = graph.invoke({"request": request})

    st.success("Generated initial options")

    room_analysis = result.get("room_analysis", {})
    with st.expander("Room analysis"):
        st.json(room_analysis)

    options = result.get("options", [])
    if not options:
        st.warning("No options found.")
    else:
        cols = st.columns(len(options))
        for col, option in zip(cols, options):
            with col:
                st.markdown(f"### {option.name}")
                st.write(option.summary)
                st.metric("Estimated total", f"${option.total_price:,.0f}")
                st.caption(f"Score: {option.score:.2f}")
                for item in option.items:
                    st.markdown(
                        f"- **{item.category.title()}**: {item.name} — ${item.price:.0f} ({item.retailer})"
                    )

    with st.expander("Raw graph output"):
        st.write(result)
else:
    st.info("Set preferences in the sidebar, then generate the first draft.")