import time
from utils.audio_processing import record_audio, play_audio
from utils.aws_services import transcribe_audio, synthesize_speech, lex_conversation

def main():
    print("Welcome to AWS Voice-to-Voice Chat by MANISH SINGH!")
    
    while True:
        print("\nSpeak your message (Recording will start in 3 seconds)...")
        time.sleep(3)
        
        # Record user audio
        audio_file = "input.wav"
        record_audio(audio_file)
        print("Recording complete!")
        
        # Transcribe audio to text
        print("Transcribing your message...")
        user_text = transcribe_audio(audio_file)
        print(f"You said: {user_text}")
        
        # Pass user text to Lex for conversation
        print("Sending your message to AWS Lex...")
        lex_response = lex_conversation(user_text)
        print(f"Lex Response: {lex_response}")
        
        # Synthesize Lex response to speech
        print("Converting Lex response to speech...")
        response_audio = "response.mp3"
        synthesize_speech(lex_response, response_audio)
        
        # Play synthesized audio
        print("Playing Lex response...")
        play_audio(response_audio)
        
        # Exit condition
        if user_text.lower() in ["exit", "quit"]:
            print("Exiting Voice-to-Voice Chat. Goodbye!")
            break

if __name__ == "__main__":
    main()
