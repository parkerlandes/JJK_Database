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
    arc_vs_mahito = models.Arc(series_id=jk.series_id, arc_name="Vs Mahito Arc")
    arc_shibuya = models.Arc(series_id=jk.series_id, arc_name="Shibuya Incident Arc")
    arc_cursed_womb = models.Arc(series_id=jk.series_id, arc_name="Cursed Womb Arc")
    session.add_all([arc_vs_mahito, arc_shibuya, arc_cursed_womb])
    session.commit()


    # 5) Episodes (minimum examples)
    ep1 = models.Episode(arc_id=arc_cursed_womb.arc_id, season_number=1, episode_number=1, title="Ryomen Sukuna", synopsis="Yuji Itadori eats Sukuna's finger.")
    ep2 = models.Episode(arc_id=arc_vs_mahito.arc_id, season_number=1, episode_number=8, title="Boredom", synopsis="Introduction of Mahito.")
    ep3 = models.Episode(arc_id=arc_shibuya.arc_id, season_number=2, episode_number=28, title="Shibuya Incident", synopsis="Shibuya barrier is activated.")
    session.add_all([ep1, ep2, ep3])
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
    fight_shibuya = models.Fight(name="Gojo vs Curses at Shibuya", arc_id=arc_shibuya.arc_id, location_id=loc_shibuya.location_id, start_episode_id=ep3.episode_id, end_episode_id=ep3.episode_id)
    fight_vs_mahito = models.Fight(name="Yuji & Nanami vs Mahito", arc_id=arc_vs_mahito.arc_id, location_id=loc_tokyo.location_id, start_episode_id=ep2.episode_id, end_episode_id=ep2.episode_id)
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
