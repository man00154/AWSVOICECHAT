import boto3
from config import AWS_CONFIG, LEX_CONFIG

def transcribe_audio(audio_file, language_code="en-US"):
    transcribe = boto3.client("transcribe", **AWS_CONFIG)
    job_name = f"transcribe-job-{int(time.time())}"
    job_uri = f"file://{audio_file}"
    
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": job_uri},
        MediaFormat="wav",
        LanguageCode=language_code
    )
    
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status["TranscriptionJob"]["TranscriptionJobStatus"] in ["COMPLETED", "FAILED"]:
            break
        time.sleep(5)

    if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        return status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

def synthesize_speech(text, output_file, voice="Joanna"):
    polly = boto3.client("polly", **AWS_CONFIG)
    response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice)
    
    with open(output_file, "wb") as file:
        file.write(response["AudioStream"].read())

def lex_conversation(text):
    lex = boto3.client("lexv2-runtime", **AWS_CONFIG)
    response = lex.recognize_text(
        botId=LEX_CONFIG["bot_name"],
        botAliasId=LEX_CONFIG["bot_alias"],
        localeId="en_US",
        sessionId="12345",
        text=text
    )
    return response["messages"][0]["content"]
