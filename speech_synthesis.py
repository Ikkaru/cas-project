import sherpa_onnx
import soundfile as sf
import pygame
import numpy as np

# Configuration
MODEL_DIR = "./models"  # Change this to your model directory
OUTPUT_FILE = "output.wav"
SPEAKER_ID = 0
SPEED = 0.897

# Create TTS config
config = sherpa_onnx.OfflineTtsConfig(
    model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(
            model=f"{MODEL_DIR}/castorice_3100epoch.onnx",
            tokens=f"{MODEL_DIR}/tokens.txt",
            data_dir="./espeak-ng-data",
        ),
        num_threads=1,
        debug=False,
    ),
    max_num_sentences=1,
)

# Create TTS engine
print("Loading model...")
tts = sherpa_onnx.OfflineTts(config)

# Generate speech
def speech(response):
    # Initialize mixer
    pygame.mixer.init()
    
    audio = tts.generate(
        response, 
        sid=SPEAKER_ID, 
        speed=SPEED,
    )

    # Save audio
    samples = np.array(audio.samples, dtype=np.float32)
    sf.write(OUTPUT_FILE, samples, audio.sample_rate)

    print(f"Saved to: {OUTPUT_FILE}")
    print(f"Duration: {len(samples) / audio.sample_rate:.2f} seconds")


    # Play Audio
    pygame.mixer.music.load('output.wav')
    pygame.mixer.music.play()

    # Keep the program running until music finishes
    while pygame.mixer.music.get_busy():    
        pygame.time.Clock().tick(10)
    
    # Stop any currently playing audio
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    