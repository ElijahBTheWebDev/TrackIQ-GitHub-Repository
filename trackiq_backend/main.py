import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
from sqlalchemy.exc import IntegrityError

from . import database, models, schemas, audio_processor

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CORS Middleware
origins = [
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "uploaded_audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'.mp3', '.wav', '.ogg', '.flac', '.m4a'}

def is_valid_audio_file(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    features = audio_processor.process_audio(file_path)
    audio_record = models.AudioFeatures(filename=file.filename, **features)

    db.add(audio_record)
    db.commit()
    db.refresh(audio_record)

    return {"id": audio_record.id, "filename": audio_record.filename}

@app.post("/process-mp3/")
async def process_mp3(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Validate file extension
        if not is_valid_audio_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Save the uploaded file
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Process the audio
        try:
            features = audio_processor.process_audio(file_location)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing audio file: {str(e)}"
            )
        finally:
            # Clean up the uploaded file
            if os.path.exists(file_location):
                os.remove(file_location)
        
        # Create database entry
        db_features = models.AudioFeatures(
            filename=file.filename,
            tempo=features["tempo"],
            onset_strength=features["onset_strength"],
            chroma_stft=features["chroma_stft"],
            zero_crossing_rate=features["zero_crossing_rate"],
            rms=features["rms"],
            harmonic_rms=features["harmonic_rms"],
            percussive_rms=features["percussive_rms"],
            spectral_centroid=features["spectral_centroid"],
            spectral_rolloff=features["spectral_rolloff"],
            spectral_flux=features["spectral_flux"],
            spectral_crest=features["spectral_crest"],
            spectral_complexity=features["spectral_complexity"],
            hpcp_mean=features["hpcp_mean"],
            mfcc_mean=features["mfcc_mean"],
            spectral_flatness=features["spectral_flatness"]
        )
        
        db.add(db_features)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail=f"A file named '{file.filename}' has already been processed. Please rename the file and try again."
            )
        
        db.refresh(db_features)
        
        return features
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/features/{audio_id}", response_model=schemas.AudioFeatures)
def get_features(audio_id: int, db: Session = Depends(get_db)):
    record = db.query(models.AudioFeatures).filter(models.AudioFeatures.id == audio_id).first()
    return record
