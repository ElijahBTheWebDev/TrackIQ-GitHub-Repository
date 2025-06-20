from sqlalchemy import Column, Integer, String, Float
from .database import Base

class AudioFeatures(Base):
    __tablename__ = "audio_features"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)

    tempo = Column(Float)
    onset_strength = Column(Float)
    chroma_stft = Column(Float)
    zero_crossing_rate = Column(Float)
    rms = Column(Float)
    harmonic_rms = Column(Float)
    percussive_rms = Column(Float)

    spectral_centroid = Column(Float)
    spectral_rolloff = Column(Float)
    spectral_flux = Column(Float)
    spectral_crest = Column(Float)
    spectral_complexity = Column(Float)
    hpcp_mean = Column(Float)
    mfcc_mean = Column(Float)
    spectral_flatness = Column(Float)
