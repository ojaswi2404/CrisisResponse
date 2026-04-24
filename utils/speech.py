from io import BytesIO


def transcribe_audio(audio_file):
    if not audio_file:
        return "", "No voice recording provided."

    try:
        import speech_recognition as sr
    except ImportError:
        return "", "SpeechRecognition is not installed."

    try:
        recognizer = sr.Recognizer()
        audio_bytes = audio_file.getvalue()
        with sr.AudioFile(BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)

        languages = [
            ("en-IN", "English"),
            ("hi-IN", "Hindi"),
            ("mr-IN", "Marathi"),
            ("en-US", "English"),
        ]

        for language_code, language_name in languages:
            try:
                text = recognizer.recognize_google(audio_data, language=language_code)
                if text.strip():
                    return text, f"Voice message transcribed in {language_name}."
            except sr.UnknownValueError:
                continue
        return "", "Speech could not be understood clearly."
    except sr.RequestError:
        return "", "Speech recognition service is unavailable."
    except Exception:
        return "", "Voice recording captured, but transcription failed."
