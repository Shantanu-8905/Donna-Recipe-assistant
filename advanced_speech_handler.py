import speech_recognition as sr
import pyttsx3
import asyncio
from faster_whisper import WhisperModel
import numpy as np
import librosa
import noisereduce as nr
from typing import Optional, Tuple
import soundfile as sf
import tempfile
import os

class AdvancedSpeechHandler:
    def __init__(self, use_whisper: bool = True):
        # Set up speech recognition
        self.recognizer = sr.Recognizer()
        self.use_whisper = use_whisper
        
        # Load Whisper
        if use_whisper:
            try:
                # base model is good balance
                self.whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
                print("Whisper loaded")
            except Exception as e:
                print(f"Whisper not available: {e}")
                self.use_whisper = False
        
        # Setup text-to-speech
        self.engine = pyttsx3.init()
        
        # Configure voice
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.95)
        
        # Noise reduction
        self.apply_noise_reduction = True
    
    def preprocess_audio(self, audio_data) -> np.ndarray:
        """Clean up audio"""
        # Convert to array
        audio_array = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
        
        # Convert to float
        audio_float = audio_array.astype(np.float32) / 32768.0
        
        if self.apply_noise_reduction:
            # Reduce noise
            audio_float = nr.reduce_noise(
                y=audio_float, 
                sr=audio_data.sample_rate,
                stationary=True
            )
        
        return audio_float
    
    def speak(self, text: str, rate: Optional[int] = None):
        """Say text out loud"""
        print(f"\n🤖 Donna: {text}\n")
        
        if rate:
            self.engine.setProperty('rate', rate)
        
        self.engine.say(text)
        self.engine.runAndWait()
        
        # Reset rate
        if rate:
            self.engine.setProperty('rate', 150)
    
    def listen_whisper(self, timeout: int = 7) -> Tuple[Optional[str], float]:
        """Listen using Whisper"""
        with sr.Microphone() as source:
            print("🎤 Listening... (Whisper)")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                # Save to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
                    temp_file = f.name
                    with open(temp_file, 'wb') as audio_file:
                        audio_file.write(audio.get_wav_data())
                
                # Transcribe
                segments, info = self.whisper_model.transcribe(
                    temp_file, 
                    beam_size=5,
                    language="en"
                )
                
                # Get result
                text = " ".join([segment.text for segment in segments]).strip()
                
                # Clean up
                os.unlink(temp_file)
                
                if text:
                    print(f"✅ You said: {text}")
                    # Estimate confidence
                    confidence = min(0.95, 0.7 + (len(text.split()) * 0.05))
                    return text.lower(), confidence
                
                return None, 0.0
                
            except Exception as e:
                print(f"Whisper error: {e}")
                return None, 0.0
    
    def listen_google(self, timeout: int = 7) -> Tuple[Optional[str], float]:
        """Fallback to Google"""
        with sr.Microphone() as source:
            print("🎤 Listening... (Google ASR)")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                # Try Google recognition with show_all for confidence
                result = self.recognizer.recognize_google(audio, show_all=True)
                
                if result and 'alternative' in result:
                    text = result['alternative'][0]['transcript']
                    confidence = result['alternative'][0].get('confidence', 0.85)
                    
                    print(f"✅ You said: {text}")
                    return text.lower(), confidence
                
                return None, 0.0
                
            except sr.WaitTimeoutError:
                print("⏱️ No speech detected")
                return None, 0.0
            except sr.UnknownValueError:
                print("❓ Could not understand audio")
                return None, 0.0
            except sr.RequestError as e:
                print(f"❌ API error: {e}")
                return None, 0.0
    
    def listen(self, timeout: int = 7, min_confidence: float = 0.7) -> Tuple[Optional[str], float]:
        """Listen with fallback"""
        text, confidence = None, 0.0
        
        # Try Whisper first
        if self.use_whisper:
            text, confidence = self.listen_whisper(timeout)
            
            if text and confidence >= min_confidence:
                return text, confidence
            
            print("Confidence too low, trying Google...")
        
        # Fallback to Google
        text_google, confidence_google = self.listen_google(timeout)
        
        # Return best result
        if confidence_google > confidence:
            return text_google, confidence_google
        
        return text, confidence
    
    def confirm_understanding(self, text: str) -> bool:
        """Confirm what was heard"""
        self.speak(f"I heard: {text}. Is that correct?")
        
        response, conf = self.listen(timeout=5)
        
        if response and any(word in response for word in ['yes', 'yeah', 'correct', 'right', 'yep']):
            return True
        
        return False