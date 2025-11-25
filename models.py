# models.py
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Date,
    ForeignKey, CheckConstraint, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship

from database import Base


class Series(Base):
    __tablename__ = "series"

    series_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    author = Column(String(100))
    media_type = Column(String(50))

    arcs = relationship("Arc", back_populates="series", cascade="all, delete-orphan")


class Arc(Base):
    __tablename__ = "arc"

    arc_id = Column(Integer, primary_key=True, autoincrement=True)
    series_id = Column(Integer, ForeignKey("series.series_id"), nullable=False)
    arc_name = Column(String(100), nullable=False)
    description = Column(Text)
    start_episode = Column(Integer)
    end_episode = Column(Integer)

    series = relationship("Series", back_populates="arcs")
    episodes = relationship("Episode", back_populates="arc")
    fights = relationship("Fight", back_populates="arc")


class Episode(Base):
    __tablename__ = "episode"

    episode_id = Column(Integer, primary_key=True, autoincrement=True)
    arc_id = Column(Integer, ForeignKey("arc.arc_id"), nullable=False)
    season_number = Column(Integer)
    episode_number = Column(Integer)
    title = Column(String(150), nullable=False)
    synopsis = Column(Text)

    arc = relationship("Arc", back_populates="episodes")
    fights_start = relationship(
        "Fight", back_populates="start_episode",
        foreign_keys="Fight.start_episode_id"
    )
    fights_end = relationship(
        "Fight", back_populates="end_episode",
        foreign_keys="Fight.end_episode_id"
    )


class Location(Base):
    __tablename__ = "location"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    type = Column(String(50))
    city = Column(String(100))
    country = Column(String(100))

    fights = relationship("Fight", back_populates="location")


class Clan(Base):
    __tablename__ = "clan"

    clan_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    members = relationship("Character", back_populates="clan")


class CursedTechnique(Base):
    __tablename__ = "cursed_technique"

    technique_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    users = relationship("CharacterTechnique", back_populates="technique")


class CharacterTechnique(Base):
    __tablename__ = "character_technique"

    technique_id = Column(Integer, ForeignKey("cursed_technique.technique_id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.character_id"), primary_key=True)
    is_innate = Column(Boolean, nullable=False, default=False)

    technique = relationship("CursedTechnique", back_populates="users")
    character = relationship("Character", back_populates="techniques")


class Character(Base):
    __tablename__ = "character"

    character_id = Column(Integer, primary_key=True, autoincrement=True)
    clan_id = Column(Integer, ForeignKey("clan.clan_id"))
    name = Column(String(100), nullable=False)
    grade = Column(String(50))
    description = Column(Text)
    first_appearance_episode_id = Column(Integer, ForeignKey("episode.episode_id"))
    technique_id = Column(Integer, ForeignKey("cursed_technique.technique_id"))
    is_curse = Column(Boolean, nullable=False, default=False)

    __table_args__ = (
        Index("ix_character_name", "name"),
        CheckConstraint(
            "grade IN ('Special Grade', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Semi Grade 1', 'Semi Grade 2', 'None')",
            name="ck_character_grade_valid"
        ),
    )

    clan = relationship("Clan", back_populates="members")
    first_appearance = relationship("Episode", foreign_keys=[first_appearance_episode_id])
    techniques = relationship("CharacterTechnique", back_populates="character", cascade="all, delete-orphan")
    domain = relationship("Domain", back_populates="owner", uselist=False)
    inherited_techniques = relationship("InheritedTechnique", back_populates="character", cascade="all, delete-orphan")
    fights = relationship("FightParticipant", back_populates="character", cascade="all, delete-orphan")



class Domain(Base):
    __tablename__ = "domain"

    domain_id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey("character.character_id"), unique=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    owner = relationship("Character", back_populates="domain")


class InheritedTechnique(Base):
    __tablename__ = "inherited_technique"

    inherited_technique_id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey("character.character_id"))
    name = Column(String(100), nullable=False)
    description = Column(Text)

    character = relationship("Character", back_populates="inherited_techniques")


class Fight(Base):
    __tablename__ = "fight"

    fight_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    arc_id = Column(Integer, ForeignKey("arc.arc_id"))
    location_id = Column(Integer, ForeignKey("location.location_id"))
    start_episode_id = Column(Integer, ForeignKey("episode.episode_id"))
    end_episode_id = Column(Integer, ForeignKey("episode.episode_id"))
    summary = Column(Text)

    arc = relationship("Arc", back_populates="fights")
    location = relationship("Location", back_populates="fights")
    start_episode = relationship("Episode", foreign_keys=[start_episode_id], back_populates="fights_start")
    end_episode = relationship("Episode", foreign_keys=[end_episode_id], back_populates="fights_end")
    participants = relationship("FightParticipant", back_populates="fight", cascade="all, delete-orphan")


class FightParticipant(Base):
    __tablename__ = "fight_participant"

    fight_id = Column(Integer, ForeignKey("fight.fight_id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.character_id"), primary_key=True)
    outcome = Column(String(50))

    fight = relationship("Fight", back_populates="participants")
    character = relationship("Character", back_populates="fights")
