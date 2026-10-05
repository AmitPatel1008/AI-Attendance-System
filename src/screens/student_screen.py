import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    st.space()

    c1, c2 = st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid, {"total": 0, "attended": 0})

        def unenroll_button(sid=sid, sub=sub):
            if st.button("Unenroll from this course", key=f"unenroll_{sid}", type='tertiary', width='stretch', icon=':material/delete_forever:'):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f"Unenrolled from {sub['name']} successfully!")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )

    footer_dashboard()


def student_screen():

    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False
    if "scan_result" not in st.session_state:
        st.session_state.scan_result = None
    if "last_photo_id" not in st.session_state:
        st.session_state.last_photo_id = None

    style_background_dashboard()
    style_base_layout()

    st.markdown("""
    <style>
    div[data-testid="stCameraInput"] label p,
    div[data-testid="stCameraInput"] label {
        color: #5865F2 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    div[data-testid="stSpinner"] p,
    div[data-testid="stSpinner"] span {
        color: #5865F2 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stAlert"] p {
        color: #3b3f8c !important;
        font-weight: 600 !important;
    }
    input[type="text"] {
        background-color: #ffffff !important;
        color: #111111 !important;
        caret-color: #111111 !important;
        border: 1.5px solid #5865F2 !important;
        border-radius: 10px !important;
    }
    input::placeholder { color: #999 !important; }
    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border-radius: 10px !important;
    }
    label[data-testid="stWidgetLabel"] p {
        color: #3b3f8c !important;
        font-weight: 700 !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid #5865F2 !important;
        border-radius: 20px !important;
        background: #eceeff !important;
        padding: 1rem !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] h2 {
        font-size: 1.4rem !important;
        color: #111111 !important;
        line-height: 1.2 !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] h3 {
        color: #5865F2 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="stAudioInput"] {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        border: 1.5px solid #5865F2 !important;
        padding: 4px !important;
    }
    div[data-testid="stAudioInput"] label p {
        color: #3b3f8c !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.session_state.show_registration = False
            st.session_state.scan_result = None
            st.session_state.last_photo_id = None
            st.rerun()

    st.header('Login using FaceID', text_alignment='center')
    st.space()
    st.space()

    photo_source = st.camera_input("Position your face in the center")

    if photo_source is not None:
        photo_id = getattr(photo_source, 'file_id', str(hash(photo_source.getvalue())))

        if st.session_state.last_photo_id != photo_id:
            st.session_state.last_photo_id = photo_id
            st.session_state.show_registration = False
            st.session_state.scan_result = None

            img = np.array(Image.open(photo_source))

            with st.spinner('AI is scanning..'):
                detected, all_ids, num_faces = predict_attendance(img)
                time.sleep(0.5)

            if num_faces == 0:
                st.session_state.scan_result = 'no_face'
            elif num_faces > 1:
                st.session_state.scan_result = 'multiple'
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.session_state.scan_result = 'recognized'
                        st.toast(f"Welcome Back, {student['name']}! 👋")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.session_state.scan_result = 'unknown'
                    st.session_state.show_registration = True
            st.rerun()

    if st.session_state.scan_result == 'no_face':
        st.warning('Face not found!')
    elif st.session_state.scan_result == 'multiple':
        st.warning('Multiple faces found!')
    elif st.session_state.scan_result == 'unknown':
        st.info('Face not recognized! You might be a new student!')

    if st.session_state.show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Amit Patel')
            roll_no = st.text_input("Enter your roll number", placeholder='E.g. UEC123456')

            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your voice for voice only attendance")

            audio_data = None
            try:
                audio_data = st.audio_input('Record a short phrase like I am present, My name is Amit Patel.')
            except Exception:
                st.error('Audio input not supported in this browser. Please use Chrome or Edge.')

            if st.button('Create Account', type='primary'):
                if new_name and roll_no:
                    with st.spinner('Creating profile..'):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())
                            response_data = create_student(new_name, roll_no=roll_no, face_embedding=face_emb, voice_embedding=voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.session_state.show_registration = False
                                st.toast(f"Profile Created! Hi {new_name}!")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Couldn't capture your facial features. Please retake photo.")
                else:
                    st.warning('Please enter your name and roll number!')

    footer_dashboard()