# models/cognitive_state.py
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from database.connection import Base
from datetime import datetime


class CognitiveState(Base):
    """
    Stores long-term user cognitive / relationship intelligence.
    Used for trust, friendship, emotional state, preferences, timing patterns,
    and proactive decision-making.
    """

    __tablename__ = "cognitive_state"  # consistent table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)

    # Core relationship scores
    trust_score = Column(Float, default=0.5, nullable=False)
    friendship_score = Column(Float, default=0.5, nullable=False)

    # Last user message timestamp (critical for proactive timing)
    last_interaction = Column(DateTime, nullable=True)

    # Last time this row was updated (useful for debugging & decay logic later)
    last_updated = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Advanced / future-proof fields (JSON for flexibility)
    # Can later be replaced with proper vector columns if using pgvector or similar
    emotional_state_vector = Column(JSON, default=dict, nullable=False)
    response_preference_profile = Column(JSON, default=dict, nullable=False)
    interaction_latency_pattern = Column(JSON, default=dict, nullable=False)

    def __repr__(self):
        return (
            f"<CognitiveState(phone={self.phone_number}, "
            f"trust={self.trust_score:.2f}, "
            f"friendship={self.friendship_score:.2f}, "
            f"last_interaction={self.last_interaction})>"
        )