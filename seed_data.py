# seed_data.py
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def seed():
    session = SessionLocal()

    # 1) Series
    jk = models.Series(
        name="Jujutsu Kaisen",
        description="A high school student becomes involved with jujutsu sorcerers after ingesting a cursed object.",
        author="Gege Akutami",
        media_type="Anime/Manga"
    )
    session.add(jk)
    session.commit()


    # 2) Clans
    clan_gojo = models.Clan(name="Gojo Clan")
    clan_zenin = models.Clan(name="Zenin Clan")
    clan_kamo = models.Clan(name="Kamo Clan")
    session.add_all([clan_gojo, clan_zenin, clan_kamo])
    session.commit()


    # 3) Locations
    loc_tokyo = models.Location(name="Tokyo Jujutsu High", type="School", city="Tokyo", country="Japan")
    loc_shibuya = models.Location(name="Shibuya Station", type="Urban", city="Tokyo", country="Japan")
    loc_sendai = models.Location(name="Sendai", type="City", city="Sendai", country="Japan")
    session.add_all([loc_tokyo, loc_shibuya, loc_sendai])
    session.commit()


    # 4) Arcs 
    fearsome_womb_arc = models.Arc(series_id=jk.series_id, arc_name="Fearsome Womb Arc")
    vs_mahito_arc = models.Arc(series_id=jk.series_id, arc_name="Vs Mahito Arc")
    kyoto_goodwill_event_arc = models.Arc(series_id=jk.series_id, arc_name="Kyoto Goodwill Event Arc")
    death_painting_arc = models.Arc(series_id=jk.series_id, arc_name="Death Painting Arc")
    hidden_inventory_arc = models.Arc(series_id=jk.series_id, arc_name="Hidden Inventory Arc")
    shibuya_incident_arc = models.Arc(series_id=jk.series_id, arc_name="Shibuya Incident Arc")
    culling_game_arc = models.Arc(series_id=jk.series_id, arc_name="Culling Game Arc")
    shinjuku_showdown_arc = models.Arc(series_id=jk.series_id, arc_name="Shinjuku Showdown Arc")

    session.add_all([
        fearsome_womb_arc,
        vs_mahito_arc,
        kyoto_goodwill_event_arc,
        death_painting_arc,
        hidden_inventory_arc,
        shibuya_incident_arc,
        culling_game_arc,
        shinjuku_showdown_arc
    ])
    session.commit()


    # 5) Episodes (minimum examples)

    # FEARSOME WOMB ARC (1–8)
    ep1 = models.Episode(arc_id=fearsome_womb_arc.arc_id, season_number=1, episode_number=1, title="Ryomen Sukuna")
    ep2 = models.Episode(arc_id=fearsome_womb_arc.arc_id, season_number=1, episode_number=2, title="For Myself")
    ep3 = models.Episode(arc_id=fearsome_womb_arc.arc_id, season_number=1, episode_number=3, title="Girl of Steel")
    ep4 = models.Episode(arc_id=fearsome_womb_arc.arc_id, season_number=1, episode_number=4, title="Curse Womb Must Die")
    ep5 = models.Episode(arc_id=fearsome_womb_arc.arc_id, season_number=1, episode_number=5, title="Curse Womb Must Die II")
    ep6 = models.Episode(arc_id=fearsome_womb_arc.arc_id, season_number=1, episode_number=6, title="After Rain")
    ep7 = models.Episode(arc_id=fearsome_womb_arc.arc_id, season_number=1, episode_number=7, title="Assault")
    ep8 = models.Episode(arc_id=fearsome_womb_arc.arc_id, season_number=1, episode_number=8, title="Boredom")

    # VS MAHITO ARC (9–13)
    ep9 = models.Episode(arc_id=vs_mahito_arc.arc_id, season_number=1, episode_number=9, title="Small Fry and Reverse Retribution")
    ep10 = models.Episode(arc_id=vs_mahito_arc.arc_id, season_number=1, episode_number=10, title="Idle Death Gamble")
    ep11 = models.Episode(arc_id=vs_mahito_arc.arc_id, season_number=1, episode_number=11, title="Narrow-minded")
    ep12 = models.Episode(arc_id=vs_mahito_arc.arc_id, season_number=1, episode_number=12, title="To You, Someday")
    ep13 = models.Episode(arc_id=vs_mahito_arc.arc_id, season_number=1, episode_number=13, title="Tomorrow")

    # KYOTO GOODWILL ARC (14–21)
    ep14 = models.Episode(arc_id=kyoto_goodwill_event_arc.arc_id, season_number=1, episode_number=14, title="Kyoto Sister School Exchange Event - Group Battle 0")
    ep15 = models.Episode(arc_id=kyoto_goodwill_event_arc.arc_id, season_number=1, episode_number=15, title="Kyoto Sister School Exchange Event - Group Battle 1")
    ep16 = models.Episode(arc_id=kyoto_goodwill_event_arc.arc_id, season_number=1, episode_number=16, title="Kyoto Sister School Exchange Event - Group Battle 2")
    ep17 = models.Episode(arc_id=kyoto_goodwill_event_arc.arc_id, season_number=1, episode_number=17, title="Kyoto Sister School Exchange Event - Group Battle 3")
    ep18 = models.Episode(arc_id=kyoto_goodwill_event_arc.arc_id, season_number=1, episode_number=18, title="Sage")
    ep19 = models.Episode(arc_id=kyoto_goodwill_event_arc.arc_id, season_number=1, episode_number=19, title="Black Flash")
    ep20 = models.Episode(arc_id=kyoto_goodwill_event_arc.arc_id, season_number=1, episode_number=20, title="Nonstandard")
    ep21 = models.Episode(arc_id=kyoto_goodwill_event_arc.arc_id, season_number=1, episode_number=21, title="Jujutsu Koshien")
    
    # DEATH PAINTING ARC (22–24)
    ep22 = models.Episode(arc_id=death_painting_arc.arc_id, season_number=1, episode_number=22, title="The Origin of Blind Obedience")
    ep23 = models.Episode(arc_id=death_painting_arc.arc_id, season_number=1, episode_number=23, title="The Origin of Blind Obedience II")
    ep24 = models.Episode(arc_id=death_painting_arc.arc_id, season_number=1, episode_number=24, title="Accomplices")
    
    # HIDDEN INVENTORY ARC (25–29)
    ep25 = models.Episode(arc_id=hidden_inventory_arc.arc_id, season_number=1, episode_number=25, title="Hidden Inventory I")
    ep26 = models.Episode(arc_id=hidden_inventory_arc.arc_id, season_number=1, episode_number=26, title="Hidden Inventory II")
    ep27 = models.Episode(arc_id=hidden_inventory_arc.arc_id, season_number=1, episode_number=27, title="Hidden Inventory III")
    ep28 = models.Episode(arc_id=hidden_inventory_arc.arc_id, season_number=1, episode_number=28, title="Hidden Inventory IV")
    ep29 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=29, title="Premature Death")
    
    # SHIBUYA INCIDENT ARC (30–47)
    ep30 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=30, title="It's Like That")
    ep31 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=31, title="Evening Festival")
    ep32 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=32, title="The Shibuya Incident")
    ep33 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=33, title="Shibuya Incident – Gate, Open")
    ep34 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=34, title="Pandemonium")
    ep35 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=35, title="Seance")
    ep36 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=36, title="Dull Knife")
    ep37 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=37, title="Red Scale")
    ep38 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=38, title="Fluctuations")
    ep39 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=39, title="Fluctuations, Part 2")
    ep40 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=40, title="Thunderclap")
    ep41 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=41, title="Thunderclap, Part 2")
    ep42 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=42, title="Right and Wrong")
    ep43 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=43, title="Right and Wrong, Part 2")
    ep44 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=44, title="Right and Wrong, Part 3")
    ep45 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=45, title="Metamorphosis")
    ep46 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=46, title="Metamorphosis, Part 2")
    ep47 = models.Episode(arc_id=shibuya_incident_arc.arc_id, season_number=1, episode_number=47, title="Shibuya Incident – Gate, Close")

    session.add_all([
        ep1, ep2, ep3, ep4, ep5, ep6, ep7, ep8,
        ep9, ep10, ep11, ep12, ep13,
        ep14, ep15, ep16, ep17, ep18, ep19, ep20, ep21,
        ep22, ep23, ep24,
        ep25, ep26, ep27, ep28, ep29,
        ep30, ep31, ep32, ep33, ep34, ep35, ep36, ep37,
        ep38, ep39, ep40, ep41, ep42, ep43, ep44,
        ep45, ep46, ep47
    ])
    session.commit()


    # 5b) Arc Episodes
    fearsome_womb_arc.start_episode_id = ep1.episode_id
    fearsome_womb_arc.end_episode_id   = ep8.episode_id

    vs_mahito_arc.start_episode_id = ep9.episode_id
    vs_mahito_arc.end_episode_id   = ep13.episode_id

    kyoto_goodwill_event_arc.start_episode_id = ep14.episode_id
    kyoto_goodwill_event_arc.end_episode_id   = ep21.episode_id

    death_painting_arc.start_episode_id = ep22.episode_id
    death_painting_arc.end_episode_id   = ep24.episode_id

    hidden_inventory_arc.start_episode_id = ep25.episode_id
    hidden_inventory_arc.end_episode_id   = ep29.episode_id

    shibuya_incident_arc.start_episode_id = ep30.episode_id
    shibuya_incident_arc.end_episode_id   = ep47.episode_id

    session.commit()


    # 6) Cursed Techniques
    tech_limitless = models.CursedTechnique(name="Limitless", description="Manipulation of space at the atomic level.")
    tech_six_eyes = models.CursedTechnique(name="Six Eyes", description="Extreme perception ability allowing precise cursed energy control.")
    tech_divergent_fist = models.CursedTechnique(name="Divergent Fist", description="Yuji’s delayed-impact double strike.")
    tech_ten_shadows = models.CursedTechnique(name="Ten Shadows", description="Shikigami summoning with cursed energy.")
    tech_idle_transfiguration = models.CursedTechnique(name="Idle Transfiguration", description="Mahito reshapes souls.")
    session.add_all([tech_limitless, tech_six_eyes, tech_divergent_fist, tech_ten_shadows, tech_idle_transfiguration])
    session.commit()


    # 7) Characters
    gojo = models.Character(name="Satoru Gojo", clan_id=clan_gojo.clan_id, grade="Special Grade", description="Strongest sorcerer", is_curse=False)
    yuji = models.Character(name="Yuji Itadori", clan_id=None, grade="Grade 2", description="Host of Sukuna", is_curse=False)
    megumi = models.Character(name="Megumi Fushiguro", clan_id=clan_zenin.clan_id, grade="Grade 2", description="Ten Shadows user", is_curse=False)
    sukuna = models.Character(name="Ryomen Sukuna", clan_id=None, grade="Special Grade", description="King of Curses", is_curse=True)
    mahito = models.Character(name="Mahito", clan_id=None, grade="Special Grade", description="Curse who reshapes souls", is_curse=True)
    session.add_all([gojo, yuji, megumi, sukuna, mahito])
    session.commit()


    # 8) Character Techniques (M:N)
    session.add_all([
        models.CharacterTechnique(character_id=gojo.character_id, technique_id=tech_limitless.technique_id),
        models.CharacterTechnique(character_id=gojo.character_id, technique_id=tech_six_eyes.technique_id),
        models.CharacterTechnique(character_id=yuji.character_id, technique_id=tech_divergent_fist.technique_id),
        models.CharacterTechnique(character_id=megumi.character_id, technique_id=tech_ten_shadows.technique_id),
        models.CharacterTechnique(character_id=mahito.character_id, technique_id=tech_idle_transfiguration.technique_id),
    ])
    session.commit()


    # 9) Domains
    domain_void = models.Domain(character_id=gojo.character_id, name="Unlimited Void", description="Infinite space overloads perception.")
    domain_shrine = models.Domain(character_id=sukuna.character_id, name="Malevolent Shrine", description="Slashing domain with no barrier.")
    session.add_all([domain_void, domain_shrine])
    session.commit()


    # 10) Inherited Techniques
    inh_ten_shadows = models.InheritedTechnique(character_id=megumi.character_id, name="Inherited: Ten Shadows", description="Passed through Zenin lineage.")
    inh_limitless = models.InheritedTechnique(character_id=gojo.character_id, name="Inherited: Limitless", description="Passed within Gojo clan.")
    session.add_all([inh_ten_shadows, inh_limitless])
    session.commit()


    # 11) Fights
    fight_shibuya = models.Fight(name="Gojo vs Curses at Shibuya", arc_id=shibuya_incident_arc.arc_id, location_id=loc_shibuya.location_id, start_episode_id=ep3.episode_id, end_episode_id=ep3.episode_id)
    fight_vs_mahito = models.Fight(name="Yuji & Nanami vs Mahito", arc_id=vs_mahito_arc.arc_id, location_id=loc_tokyo.location_id, start_episode_id=ep2.episode_id, end_episode_id=ep2.episode_id)
    session.add_all([fight_shibuya, fight_vs_mahito])
    session.commit()


    # 12) Fight Participants (M:N)
    session.add_all([
        models.FightParticipant(fight_id=fight_shibuya.fight_id, character_id=gojo.character_id, outcome="Victory"),
        models.FightParticipant(fight_id=fight_shibuya.fight_id, character_id=mahito.character_id, outcome="Defeat"),
        models.FightParticipant(fight_id=fight_vs_mahito.fight_id, character_id=yuji.character_id, outcome="Survived"),
        models.FightParticipant(fight_id=fight_vs_mahito.fight_id, character_id=mahito.character_id, outcome="Escaped"),
    ])
    session.commit()

    session.close()
    print("Database populated successfully!")


if __name__ == "__main__":
    seed()
