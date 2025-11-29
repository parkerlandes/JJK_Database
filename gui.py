import streamlit as st
from database import SessionLocal
import models
from llm_query import answer_query

session = SessionLocal()

st.set_page_config(page_title="JJK Database", layout="wide")

# =======================
# SIDEBAR NAVIGATION
# =======================
page = st.sidebar.radio("Navigate", [
    "Characters",
    "Arcs",
    "Episodes",
    "Fights",
    "Domains",
    "Techniques",
    "Clans",
    "Locations",
    "AI Query"
])

# =======================
# CHARACTERS PAGE
# =======================
if page == "Characters":
    st.title("Characters")

    chars = session.query(models.Character).all()
    episodes = session.query(models.Episode).order_by(models.Episode.episode_number.asc()).all()
    clans = session.query(models.Clan).all()
    techs = session.query(models.CursedTechnique).all()

    for c in chars:
        with st.expander(c.name):

            # ========= BASIC INFO ==========
            clan = session.query(models.Clan).filter_by(clan_id=c.clan_id).first()
            clan_name = clan.name if clan else "None"

            # First appearance
            if c.first_appearance_episode_id:
                ep = session.query(models.Episode).filter_by(
                    episode_id=c.first_appearance_episode_id).first()
                ep_text = f"Episode {ep.episode_number}: {ep.title}"
            else:
                ep_text = "Not Set"

            st.write(f"**Grade:** {c.grade}")
            st.write(f"**Description:** {c.description}")
            st.write(f"**Clan:** {clan_name}")
            st.write(f"**First Appearance:** {ep_text}")
            st.write(f"**Is Curse:** {c.is_curse}")

            # ========= TECHNIQUES ==========
            st.write("### Techniques")

            char_techs = session.query(models.CharacterTechnique).filter_by(
                character_id=c.character_id).all()

            if char_techs:
                for ct in char_techs:
                    t = session.query(models.CursedTechnique).filter_by(
                        technique_id=ct.technique_id).first()

                    type_str = "Innate" if ct.is_innate else "Learned"
                    st.write(f"- {t.name} ({type_str})")

            else:
                st.write("No registered techniques.")

            # ========= DOMAINS ==========
            st.write("### Domain Expansions")

            domains = session.query(models.Domain).filter_by(
                character_id=c.character_id).all()

            if domains:
                for d in domains:
                    st.write(f"- {d.name}: {d.description}")
            else:
                st.write("No domain registered.")

            st.divider()
            st.subheader("Character Actions")

            # ================================
            # ASSIGN FIRST APPEARANCE
            # ================================
            with st.expander("Assign First Appearance Episode"):
                ep_select = st.selectbox(
                    f"Select Episode",
                    [f"Episode {e.episode_number}: {e.title}" for e in episodes],
                    key=f"fa_ep_{c.character_id}"
                )
                if st.button(f"Set Episode for {c.name}", key=f"fa_btn_{c.character_id}"):
                    ep_num = int(ep_select.split(" ")[1].replace(":", ""))
                    ep_obj = session.query(models.Episode).filter_by(episode_number=ep_num).first()
                    c.first_appearance_episode_id = ep_obj.episode_id
                    session.commit()
                    st.success(f"{c.name} first appeared in Episode {ep_num}")

            # ================================
            # ASSIGN TECHNIQUE
            # ================================
            with st.expander("Assign Technique to Character"):
                t_select = st.selectbox(
                    "Technique",
                    [t.name for t in techs],
                    key=f"tech_sel_{c.character_id}"
                )
                is_innate = st.checkbox("Innate Ability?", key=f"tech_innate_{c.character_id}")

                if st.button(f"Assign Technique to {c.name}", key=f"assigntech_{c.character_id}"):
                    t_obj = session.query(models.CursedTechnique).filter_by(name=t_select).first()

                    link = models.CharacterTechnique(
                        character_id=c.character_id,
                        technique_id=t_obj.technique_id,
                        is_innate=is_innate
                    )
                    session.add(link)
                    session.commit()
                    st.success(f"{t_select} assigned to {c.name}")

            # ================================
            # ASSIGN CHARACTER TO CLAN
            # ================================
            with st.expander("Assign Character to Clan"):

                clan_select = st.selectbox(
                    "Select Clan",
                    [cl.name for cl in clans],
                    key=f"clan_sel_{c.character_id}"
                )

                if st.button(f"Assign Clan to {c.name}", key=f"assignclan_{c.character_id}"):
                    clan_obj = session.query(models.Clan).filter_by(name=clan_select).first()
                    c.clan_id = clan_obj.clan_id
                    session.commit()
                    st.success(f"{c.name} assigned to clan {clan_select}")

            # ================================
            # REMOVE CHARACTER FROM CLAN
            # ================================
            with st.expander("Remove Character from Clan"):
                if c.clan_id:
                    if st.button(f"Remove from Clan", key=f"removeclan_{c.character_id}"):
                        c.clan_id = None
                        session.commit()
                        st.success(f"{c.name} removed from clan")
                else:
                    st.info(f"{c.name} is not currently in a clan")

            # ================================
            # DELETE CHARACTER
            # ================================
            with st.expander("Delete Character"):
                st.warning(f"This action will permanently remove {c.name}!")
                if st.button(f"Delete {c.name}", key=f"deletechar_{c.character_id}"):
                    session.delete(c)
                    session.commit()
                    st.success(f"{c.name} deleted!")

    st.divider()

    # ================================
    # CREATE NEW CHARACTER
    # ================================
    st.subheader("Add New Character")
    new_name = st.text_input("Character Name")
    grade = st.text_input("Grade")
    desc = st.text_area("Description")

    if st.button("Create Character", key="newchar"):
        c = models.Character(name=new_name, grade=grade, description=desc)
        session.add(c)
        session.commit()
        st.success(f"Added {new_name}!")



# =======================
# ARCS PAGE
# =======================
elif page == "Arcs":
    st.title("Arcs")

    arcs = session.query(models.Arc).all()
    for a in arcs:
        with st.expander(a.arc_name):

            st.write(f"**Description:** {a.description}")

            # Get episodes
            episodes = session.query(models.Episode).filter_by(arc_id=a.arc_id).order_by(models.Episode.episode_number).all()

            if episodes:
                st.write("### Episodes:")
                for e in episodes:
                    with st.expander(f"S{e.season_number}E{e.episode_number}: {e.title}"):

                        st.write(f"**Title:** {e.title}")
                        st.write(f"**Synopsis:** {e.synopsis}")

                        # =====================
                        # Characters in episode
                        # =====================
                        chars_in_ep = session.query(models.Character).filter(
                            models.Character.first_appearance_episode_id <= e.episode_id
                        ).all()

                        if chars_in_ep:
                            st.write("**Characters Appearing:**")
                            for c in chars_in_ep:
                                st.write(f"- {c.name}")
                        else:
                            st.write("_No characters found for this episode._")

                        # =====================
                        # Fights in episode
                        # =====================
                        fights_in_ep = session.query(models.Fight).filter(
                            models.Fight.start_episode_id <= e.episode_id,
                            models.Fight.end_episode_id >= e.episode_id
                        ).all()

                        if fights_in_ep:
                            st.write("**Fights:**")
                            for f in fights_in_ep:
                                st.write(f"- {f.name}")
                        else:
                            st.write("_No fights found for this episode._")

            else:
                st.write("_No episodes found for this arc._")

    st.divider()

    st.subheader("Add Arc")
    series_list = session.query(models.Series).all()
    series = st.selectbox("Series", [x.name for x in series_list])
    series_obj = session.query(models.Series).filter_by(name=series).first()
    arc_name = st.text_input("Arc Name")
    arc_desc = st.text_area("Description")
    if st.button("Create Arc"):
        a = models.Arc(series_id=series_obj.series_id, arc_name=arc_name, description=arc_desc)
        session.add(a)
        session.commit()
        st.success(f"Arc {arc_name} added!")



# =======================
# EPISODES PAGE
# =======================
elif page == "Episodes":
    st.title("Episodes")

    episodes = session.query(models.Episode).order_by(
        models.Episode.season_number,
        models.Episode.episode_number
    ).all()

    for e in episodes:
        with st.expander(f"S{e.season_number}E{e.episode_number}: {e.title}"):

            st.write(f"**Title:** {e.title}")
            st.write(f"**Synopsis:** {e.synopsis}")

            # --- ARC NAME ---
            arc_obj = session.query(models.Arc).filter_by(arc_id=e.arc_id).first()
            if arc_obj:
                st.write(f"**Arc:** {arc_obj.arc_name}")
            else:
                st.write("**Arc:** Unknown")

            # --- CHARACTERS APPEARING ---
            chars_in_ep = session.query(models.Character).filter(
                models.Character.first_appearance_episode_id <= e.episode_id
            ).all()

            st.write("**Characters Appearing:**")
            if chars_in_ep:
                for c in chars_in_ep:
                    # attempt to resolve clan
                    if c.clan_id:
                        clan = session.query(models.Clan).filter_by(clan_id=c.clan_id).first()
                        clan_name = clan.name if clan else "Unknown"
                    else:
                        clan_name = "None"

                    st.write(f"- {c.name} (Clan: {clan_name}, Grade: {c.grade})")
            else:
                st.write("_No character data for this episode._")

            # --- FIGHTS IN EPISODE ---
            fights_in_ep = session.query(models.Fight).filter(
                models.Fight.start_episode_id <= e.episode_id,
                models.Fight.end_episode_id >= e.episode_id
            ).all()

            st.write("**Fights:**")
            if fights_in_ep:
                for f in fights_in_ep:
                    st.write(f"- {f.name}")
            else:
                st.write("_No fights in this episode._")


    st.divider()

    # ---------- Add Episode ----------
    st.subheader("Add Episode")

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
        st.success(f"Episode {title} added!")



# =======================
# FIGHTS PAGE
# =======================
elif page == "Fights":
    st.title("Fights")

    fights = session.query(models.Fight).order_by(models.Fight.start_episode_id.asc()).all()

    if not fights:
        st.write("No fights found.")
    else:
        for f in fights:
            arc = session.query(models.Arc).filter_by(arc_id=f.arc_id).first()
            loc = session.query(models.Location).filter_by(location_id=f.location_id).first()
            ep_start = session.query(models.Episode).filter_by(episode_id=f.start_episode_id).first()
            ep_end = session.query(models.Episode).filter_by(episode_id=f.end_episode_id).first()
            participants = session.query(models.FightParticipant).filter_by(fight_id=f.fight_id).all()

            with st.expander(f"{f.name}"):

                st.write(f"**Arc:** {arc.arc_name}")
                st.write(f"**Location:** {loc.name}")
                st.write(f"**Episode Range:** {ep_start.episode_number} – {ep_end.episode_number}")
                st.write(f"**Summary:** {f.summary}")

                st.write("### Participants:")
                for p in participants:
                    char = session.query(models.Character).filter_by(character_id=p.character_id).first()
                    st.write(f"- {char.name}: **{p.outcome.upper()}**")

                # DELETE BUTTON
                if st.button(f"Delete Fight: {f.name}", key=f"delete_fight_{f.fight_id}"):
                    
                    # delete participants first
                    session.query(models.FightParticipant).filter_by(fight_id=f.fight_id).delete()
                    
                    # delete fight
                    session.delete(f)
                    session.commit()
                    st.success(f"Deleted fight '{f.name}'")

    st.divider()

    # ---------- ADD FIGHT ----------
    st.subheader("Add Fight")

    fight_name = st.text_input("Fight Name")
    arc_list = session.query(models.Arc).all()
    selected_arc = st.selectbox("Arc", [x.arc_name for x in arc_list])
    selected_arc_obj = session.query(models.Arc).filter_by(arc_name=selected_arc).first()

    loc_list = session.query(models.Location).all()
    selected_loc = st.selectbox("Location", [x.name for x in loc_list])
    selected_loc_obj = session.query(models.Location).filter_by(name=selected_loc).first()

    start_ep = st.number_input("Start Episode", min_value=1)
    end_ep = st.number_input("End Episode", min_value=1)
    summary = st.text_area("Summary")

    if st.button("Create Fight"):
        new_f = models.Fight(
            name=fight_name,
            arc_id=selected_arc_obj.arc_id,
            location_id=selected_loc_obj.location_id,
            start_episode_id=start_ep,
            end_episode_id=end_ep,
            summary=summary
        )
        session.add(new_f)
        session.commit()
        st.success(f"Fight '{fight_name}' added!")

# =======================
# DOMAINS PAGE
# =======================
elif page == "Domains":
    st.title("Domains")

    # ========= VIEW EXISTING DOMAINS =========
    domains = session.query(models.Domain).all()

    if not domains:
        st.write("No domains exist.")
    else:
        for d in domains:
            char = session.query(models.Character).filter_by(character_id=d.character_id).first()

            with st.expander(d.name):
                st.write(f"**Used By:** {char.name if char else 'Unassigned'}")
                st.write(f"**Description:** {d.description}")

    st.divider()

    # ========= ADD DOMAIN =========
    st.subheader("Add New Domain")

    new_dom_name = st.text_input("Domain Name")

    chars = session.query(models.Character).all()
    selected_char = st.selectbox(
        "Character Who Uses This Domain",
        [c.name for c in chars]
    )

    selected_char_obj = session.query(models.Character).filter_by(name=selected_char).first()

    
    new_dom_desc = st.text_area("Domain Description")

    if st.button("Create Domain"):
        dom = models.Domain(
            character_id=selected_char_obj.character_id,
            name=new_dom_name,
            description=new_dom_desc
        )
        session.add(dom)
        session.commit()
        st.success(f"Domain '{new_dom_name}' assigned to {selected_char}!")


# =======================
# TECHNIQUES PAGE
# =======================
elif page == "Techniques":
    st.title("Cursed Techniques")

    techs = session.query(models.CursedTechnique).all()

    # -------- VIEW TECHNIQUES --------
    for t in techs:
        with st.expander(f"{t.name}"):

            st.write(f"**Description:** {t.description}")

            # list users of this technique
            users = session.query(models.CharacterTechnique).filter_by(
                technique_id=t.technique_id
            ).all()

            if users:
                st.write("### Users:")
                for ct in users:
                    char = session.query(models.Character).filter_by(
                        character_id=ct.character_id
                    ).first()

                    type_str = "Innate" if ct.is_innate else "Learned"
                    st.write(f"- {char.name} ({type_str})")
            else:
                st.write("_No characters use this technique._")

    st.divider()

    # -------- ADD TECHNIQUE --------
    st.subheader("Add Technique")

    tech_name = st.text_input("Technique Name")
    tech_desc = st.text_area("Technique Description")

    if st.button("Create Technique"):
        new_t = models.CursedTechnique(
            name=tech_name,
            description=tech_desc
        )
        session.add(new_t)
        session.commit()
        st.success(f"Technique '{tech_name}' added!")



# =======================
# CLANS PAGE
# =======================
elif page == "Clans":
    st.title("Clans")

    clans = session.query(models.Clan).all()

    for clan in clans:
        with st.expander(clan.name):

            # ------------- MEMBERS -------------
            members = session.query(models.Character).filter_by(clan_id=clan.clan_id).all()

            st.write("### Members:")
            if members:
                for m in members:
                    st.write(f"- {m.name}")
            else:
                st.write("_No known members in database._")

            # ------------- DOMINANT TECHNIQUES -------------
            clan_member_ids = [m.character_id for m in members]

            if clan_member_ids:
                tech_usage = session.query(models.CharacterTechnique).filter(
                    models.CharacterTechnique.character_id.in_(clan_member_ids)
                ).all()

                tech_count = {}
                for t in tech_usage:
                    tech_count[t.technique_id] = tech_count.get(t.technique_id, 0) + 1

                # >50% threshold
                dominant_techs = [
                    tech_id for tech_id, count in tech_count.items()
                    if count >= len(members) / 2
                ]

                st.write("### Clan Techniques:")
                if dominant_techs:
                    for tid in dominant_techs:
                        tech = session.query(models.CursedTechnique).filter_by(
                            technique_id=tid
                        ).first()
                        st.write(f"- {tech.name}")
                else:
                    st.write("_No common clan-wide techniques detected._")

            else:
                st.write("_No technique usage data for this clan._")

    st.divider()

    # ------------- ADD CLAN -------------
    st.subheader("Add Clan")
    new_clan = st.text_input("Clan Name")
    if st.button("Create Clan"):
        session.add(models.Clan(name=new_clan))
        session.commit()
        st.success(f"Clan '{new_clan}' added!")


# =======================
# LOCATIONS PAGE
# =======================
elif page == "Locations":
    st.title("Locations")

    locations = session.query(models.Location).all()

    for loc in locations:
        with st.expander(loc.name):

            # BASIC INFO
            st.write(f"**Name:** {loc.name}")
            st.write(f"**Type:** {loc.type}")
            st.write(f"**City:** {loc.city}")
            st.write(f"**Country:** {loc.country}")

            # FIGHTS HERE
            fights_here = session.query(models.Fight).filter_by(location_id=loc.location_id).all()

            st.write("### Fights at this location:")
            if fights_here:
                for f in fights_here:
                    arc = session.query(models.Arc).filter_by(arc_id=f.arc_id).first()
                    ep1 = session.query(models.Episode).filter_by(episode_id=f.start_episode_id).first()
                    ep2 = session.query(models.Episode).filter_by(episode_id=f.end_episode_id).first()

                    ep_range = ""
                    if ep1 and ep2 and ep1.episode_number and ep2.episode_number:
                        ep_range = f" (Episodes {ep1.episode_number}–{ep2.episode_number})"

                    st.write(f"- **{f.name}** — Arc: _{arc.arc_name}_{ep_range}")
            else:
                st.write("_No fights recorded here yet._")

    st.divider()

    # ---------- Add New Location ----------
    st.subheader("Add Location")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Location Name")
        type = st.text_input("Type (Island, City, Station, School, etc.)")
    with col2:
        city = st.text_input("City")
        country = st.text_input("Country")

    if st.button("Add Location"):
        new_loc = models.Location(
            name=name,
            type=type,
            city=city,
            country=country
        )
        session.add(new_loc)
        session.commit()
        st.success(f"Location '{name}' added!")


# =======================
# AI QUERY PAGE
# =======================
elif page == "AI Query":
    st.title("AI Database Search")

    query = st.text_input("Ask a question")
    if st.button("Ask"):
        with st.spinner("Thinking…"):
            res = answer_query(query)
        st.write(res)
