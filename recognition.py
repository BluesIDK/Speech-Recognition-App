import streamlit as st
import speech_recognition as sr
import time

# Session state to hold transcript and pause flag
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'paused' not in st.session_state:
    st.session_state.paused = False


# Function to transcribe speech using selected API and language
def transcribe_speech(api_choice, language):
    recognizer = sr.Recognizer()

    # Open the microphone and listen
    with sr.Microphone() as source:
        st.info("🎙️ Speak now...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            # Capture audio
            audio = recognizer.listen(source, timeout=10)
            st.info("🧠 Transcribing...")

            # Use selected API
            if api_choice == "Google":
                text = recognizer.recognize_google(audio, language=language)
            elif api_choice == "Sphinx":
                text = recognizer.recognize_sphinx(audio, language=language)
            else:
                return "❌ Unsupported API."

            return text

        except sr.WaitTimeoutError:
            return "⚠️ Timeout: No speech detected."
        except sr.UnknownValueError:
            return "🤷 Could not understand the audio."
        except sr.RequestError as e:
            return f"🚫 API Request Error: {e}"
        except Exception as e:
            return f"❗Unexpected Error: {e}"


# Main function to run the app
def main():
    st.title("🗣️ Speech Recognition App (Upgraded)")

    st.write("This app lets you record and transcribe speech using different APIs.")

    # Select API
    api_choice = st.selectbox("Choose Speech Recognition API:", ["Google", "Sphinx"])

    # Language Selection
    language_map = {
        "English (US)": "en-US",
        "French (FR)": "fr-FR",
        "Arabic (Algeria)": "ar-DZ"
    }
    lang_choice = st.selectbox("Choose Language:", list(language_map.keys()))
    language = language_map[lang_choice]

    # Show current transcript
    st.text_area("📝 Transcript", st.session_state.transcript, height=150)

    col1, col2, col3 = st.columns(3)

    # Button to start recording
    with col1:
        if st.button("🎤 Start Recording"):
            if not st.session_state.paused:
                result = transcribe_speech(api_choice, language)
                st.session_state.transcript += result + "\n"

    # Pause/Resume logic
    with col2:
        if st.button("⏯️ Pause/Resume"):
            st.session_state.paused = not st.session_state.paused
            st.success("⏸️ Paused." if st.session_state.paused else "▶️ Resumed.")

    # Save transcript to file
    with col3:
        if st.button("💾 Save Transcript"):
            if st.session_state.transcript.strip():
                filename = f"transcript_{int(time.time())}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(st.session_state.transcript)
                st.success(f"Transcript saved as `{filename}`")
                with open(filename, "rb") as file:
                    st.download_button("⬇️ Download it", data=file, file_name=filename, mime="text/plain")
            else:
                st.warning("Nothing to save yet!")

# Run the app
if __name__ == "__main__":
    main()
