from pydantic import BaseModel

class AudioFeatures(BaseModel):
    id: int
    filename: str

    tempo: float
    onset_strength: float
    chroma_stft: float
    zero_crossing_rate: float
    rms: float
    harmonic_rms: float
    percussive_rms: float

    spectral_centroid: float
    spectral_rolloff: float
    spectral_flux: float
    spectral_crest: float
    spectral_complexity: float
    hpcp_mean: float
    mfcc_mean: float
    spectral_flatness: float

    class Config:
        orm_mode = True
