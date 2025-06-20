import numpy as np
import librosa
import essentia.standard as ess

def process_audio(file_path):
    # Load audio with librosa (auto-detects sample rate and bit depth)
    y, sr = librosa.load(file_path, sr=None)
    
    # Ensure audio length is even
    if len(y) % 2 != 0:
        y = np.pad(y, (0, 1), mode='constant')
    
    # Basic features with librosa
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    rms = librosa.feature.rms(y=y)
    harm, perc = librosa.effects.hpss(y)
    harmonic_rms = librosa.feature.rms(y=harm)
    percussive_rms = librosa.feature.rms(y=perc)

    # Essentia features
    loader = ess.MonoLoader(filename=file_path)
    audio = loader()
    
    # Ensure audio length is even for Essentia
    if len(audio) % 2 != 0:
        audio = np.pad(audio, (0, 1), mode='constant')
    
    window_size = 2048
    window = ess.Windowing(size=window_size)
    windowed_audio = window(audio)
    spectrum = ess.Spectrum()(windowed_audio)
    
    # Compute frequency bins for the spectrum
    freqs = np.linspace(0, sr / 2, len(spectrum), endpoint=False)
    hpcp = ess.HPCP()(spectrum, freqs)
    mfcc = ess.MFCC()(spectrum)
    flatness = ess.FlatnessSFX()(spectrum)
    spectral_centroid = ess.Centroid()(spectrum)
    spectral_rolloff = ess.RollOff()(spectrum)
    spectral_flux = ess.Flux()(spectrum)
    spectral_crest = ess.Crest()(spectrum)
    spectral_complexity = ess.SpectralComplexity()(spectrum)

    return {
        "tempo": float(tempo),
        "onset_strength": float(np.mean(onset_env)),
        "chroma_stft": float(np.mean(chroma)),
        "zero_crossing_rate": float(np.mean(zcr)),
        "rms": float(np.mean(rms)),
        "harmonic_rms": float(np.mean(harmonic_rms)),
        "percussive_rms": float(np.mean(percussive_rms)),
        "spectral_centroid": float(spectral_centroid),
        "spectral_rolloff": float(spectral_rolloff),
        "spectral_flux": float(spectral_flux),
        "spectral_crest": float(spectral_crest),
        "spectral_complexity": float(spectral_complexity),
        "hpcp_mean": float(np.mean(hpcp)),
        "mfcc_mean": float(np.mean(mfcc[1])),
        "spectral_flatness": float(flatness),
    }
