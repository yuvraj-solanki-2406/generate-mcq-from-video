import streamlit as st
import moviepy.editor as me
from io import BytesIO
import tempfile
import speech_recognition as sr
import google.generativeai as genai

GOOGLE_API = # 'your GOOGLE Gemini API key'
genai.configure(api_key=GOOGLE_API)


# Generate questions from Gemini
def generate_questions(txt):
    model = genai.GenerativeModel('gemini-pro')
    res = model.generate_content(txt)
    return res.text


st.title("Generate Question from Video")
st.text("Upload a Video to generate question from that Video")

num_questions = st.number_input(label="Enter number of Question to generate",
                                max_value=8, min_value=1, value=3)
video = st.file_uploader(label="Upload a Video file",
                         accept_multiple_files=False,
                         type=['mp4', 'avi', 'wmv'])

button = st.button(label="Upload Video")


if button:
    if video is not None:
        video_data = video.read()
        video_stream = BytesIO(video_data)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(video_data)
            temp_file_path = temp_file.name

        # Load the video file using MoviePy
        fl = me.VideoFileClip(temp_file_path)

        audio_file = fl.audio
        audio_file.write_audiofile(f"audios/{video.file_id}.wav")
        r = sr.Recognizer()
        with sr.AudioFile(f"audios/{video.file_id}.wav") as source:
            data = r.record(source)

        search_text = r.recognize_google(data)

        input_prompt = f'''Create "{num_questions}" MCQ questions from this
            text and the questions should be conceptual on this text
            "{search_text}".
        '''
        response = generate_questions(input_prompt)
        st.text(response)

# st.text(input_prompt)
