import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from llm_query import answer_query

def get_session():
    return SessionLocal()

session = get_session()

# =======================
# GENERAL UI
# =======================
st.set_page_config(page_title="JJK Database", layout="wide")

st.markdown("""
<style>
    .main-title {
        font-size:34px !important;
        font-weight:700 !important;
        margin-bottom:10px;
    }
    .section-title {
        font-size:22px !important;
        font-weight:600 !important;
        margin-top:25px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Jujutsu Kaisen Database</div>", unsafe_allow_html=True)


# =======================
# SIDEBAR NAVIGATION
# =======================

st.sidebar.markdown("## Database Tools")

with st.sidebar.expander("CRUD Operations", expanded=True):
    crud_action = st.radio(
        "Select Operation", 
        [
            "View Characters",
            "Add Character",
            "Add Arc",
            "Add Episode",
            "Add Domain",
            "Add Technique",
            "Delete Character"
        ],
        key="crud_select"
    )

# Persistent AI mode
if "ai_mode" not in st.session_state:
    st.session_state.ai_mode = False

if st.sidebar.button("Ask Database (AI)", key="ai_button"):
    st.session_state.ai_mode = True





# =======================
# CRUD — VIEW CHARACTERS
# =======================

if crud_action == "View Characters":
    st.markdown("<div class='section-title'>Characters</div>", unsafe_allow_html=True)

    chars = session.query(models.Character).all()

    for c in chars:
        with st.expander(f"{c.name}"):
            st.write(f"**Grade:** {c.grade}")
            st.write(f"**Description:** {c.description}")
            st.write(f"**Clan:** {c.clan_id}")
            st.write(f"**Technique:** {c.technique_id}")
            st.write(f"**First Appearance Episode:** {c.first_appearance_episode_id}")
            # st.write(f"**Is Curse:** {c.is_curse}")


# =======================
# CRUD — ADD CHARACTER
# =======================

elif crud_action == "Add Character":
    st.markdown("<div class='section-title'>Add New Character</div>", unsafe_allow_html=True)

    name = st.text_input("Name")
    grade = st.text_input("Grade")
    desc = st.text_area("Description")

    if st.button("Add Character"):
        new_char = models.Character(name=name, grade=grade, description=desc)
        session.add(new_char)
        session.commit()
        st.success("Character added.")


# =======================
# CRUD — ADD ARC
# =======================

elif crud_action == "Add Arc":
    st.markdown("<div class='section-title'>Add Arc</div>", unsafe_allow_html=True)

    series_list = session.query(models.Series).all()
    s = st.selectbox("Series", [x.name for x in series_list])

    selected_series = session.query(models.Series).filter_by(name=s).first()
    arc_name = st.text_input("Arc Name")
    arc_desc = st.text_area("Arc Description")

    if st.button("Create Arc"):
        new_arc = models.Arc(
            series_id=selected_series.series_id,
            arc_name=arc_name,
            description=arc_desc
        )
        session.add(new_arc)
        session.commit()
        st.success("Arc added.")


# =======================
# CRUD — ADD EPISODE
# =======================

elif crud_action == "Add Episode":
    st.markdown("<div class='section-title'>Add Episode</div>", unsafe_allow_html=True)

    arc_list = session.query(models.Arc).all()
    selected_arc = st.selectbox("Arc", [x.arc_name for x in arc_list])
    selected_arc_obj = session.query(models.Arc).filter_by(arc_name=selected_arc).first()

    season = st.number_input("Season Number", min_value=1)
    ep_no = st.number_input("Episode Number", min_value=1)
    title = st.text_input("Title")
    synopsis = st.text_area("Synopsis")

    if st.button("Create Episode"):
        ep = models.Episode(
            arc_id=selected_arc_obj.arc_id,
            season_number=season,
            episode_number=ep_no,
            title=title,
            synopsis=synopsis
        )
        session.add(ep)
        session.commit()
        st.success("Episode added.")


# =======================
# CRUD — ADD DOMAIN
# =======================

elif crud_action == "Add Domain":
    st.markdown("<div class='section-title'>Add Domain</div>", unsafe_allow_html=True)

    chars = session.query(models.Character).all()
    c = st.selectbox("Character", [x.name for x in chars])
    selected_char = session.query(models.Character).filter_by(name=c).first()

    dom_name = st.text_input("Domain Name")
    dom_desc = st.text_area("Domain Description")

    if st.button("Create Domain"):
        new_domain = models.Domain(
            character_id=selected_char.character_id,
            name=dom_name,
           description=dom_desc
        )
        session.add(new_domain)
        session.commit()
        st.success("Domain added.")


# =======================
# CRUD — ADD CURSED TECHNIQUE
# =======================

elif crud_action == "Add Technique":
    st.markdown("<div class='section-title'>Add Cursed Technique</div>", unsafe_allow_html=True)

    tech_name = st.text_input("Technique Name")
    tech_desc = st.text_area("Technique Description")

    if st.button("Create Technique"):
        new_t = models.CursedTechnique(
            name=tech_name,
            description=tech_desc
        )
        session.add(new_t)
        session.commit()
        st.success("Technique added.")


# =======================
# CRUD — DELETE CHARACTER
# =======================

elif crud_action == "Delete Character":
    st.markdown("<div class='section-title'>Delete Character</div>", unsafe_allow_html=True)

    chars = session.query(models.Character).all()
    selected = st.selectbox("Select character", [c.name for c in chars])

    if st.button("Delete"):
        obj = session.query(models.Character).filter_by(name=selected).first()
        session.delete(obj)
        session.commit()
        st.success("Character deleted.")


# =======================
# AI QUERY SECTION (Persistent)
# =======================

if st.session_state.ai_mode:
    st.markdown("<div class='section-title'>Ask Database (AI)</div>", unsafe_allow_html=True)
    st.write("Ask a question like: 'What clan is Megumi in?' or 'List all episodes in the Shibuya arc.'")

    if "ai_query" not in st.session_state:
        st.session_state.ai_query = ""

    query = st.text_input("Ask a question", value=st.session_state.ai_query, key="ai_text")

    # Store input on change
    st.session_state.ai_query = query

    if st.button("Ask", key="ask_ai_button"):
        with st.spinner("Querying database using AI…"):
            res = answer_query(query)
        st.write(res)