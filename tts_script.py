import streamlit as st
import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from dotenv import load_dotenv

st.set_page_config(
    page_title="Text-to-Speech App",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

translations = {
    "en": {
        "app_page_title": "TTS App",
        "app_main_title": "🎙️ Text-to-Speech (TTS) with Amazon Polly",
        "app_description": "This application converts your input text into speech using Amazon Polly.",
        "settings_header": "⚙️ Settings",
        "select_ui_language": "Select UI Language:",
        "select_voice_language": "Select TTS Language:",
        "select_voice": "Select Voice:",
        "selected_voice_info": "Selected Voice Info:",
        "voice_id_label": "Voice ID",
        "engine_label": "Engine",
        "language_label": "Language",
        "gender_label": "Gender",
        "enter_text_header": "Enter Text",
        "text_area_label": "Enter text to convert to speech here:",
        "text_area_placeholder": "Hello! Welcome to the text-to-speech application using Amazon Polly.",
        "generate_audio_button": "🎧 Generate Audio",
        "generating_audio_spinner": "Converting text to speech with {voice_name}...",
        "audio_success": "✔️ Audio successfully generated!",
        "audio_error": "❌ Audio could not be generated. Please check error messages above.",
        "no_text_warning": "⚠️ Please enter some text to convert.",
        "polly_client_error_config": "Polly client could not be initialized. Please ensure AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION) are correctly set in Streamlit Secrets or environment variables.",
        "polly_client_error_runtime": "Polly client is not available. Please check AWS configuration.",
        "polly_api_error": "Amazon Polly API error: {error}",
        "unknown_synthesis_error": "An unknown error occurred during speech synthesis: {error}",
        "no_audio_stream": "Could not retrieve audio stream from Polly.",
        "generated_audio_header": "Generated Audio",
        "download_mp3_button": "🎵 Download as MP3",
        "developer_info_header": "🧑‍💻 Developer",
        "developer_github": "GitHub",
        "developer_linkedin": "LinkedIn",
        "no_voices_for_language": "No voices available for {language_name} ({language_code}).",
        "select_valid_voice_warning": "Please select a valid voice.",
        "no_voices_from_polly_warning": "No voices could be retrieved from Amazon Polly. Please check AWS configuration and Polly service status."
    },
    "tr": {
        "app_page_title": "Metin Okuma Uygulaması",
        "app_main_title": "🎙️ Amazon Polly ile Metin Okuma (TTS)",
        "app_description": "Bu uygulama, girdiğiniz metni Amazon Polly servisini kullanarak sese dönüştürür.",
        "settings_header": "⚙️ Ayarlar",
        "select_ui_language": "Arayüz Dilini Seçin:",
        "select_voice_language": "TTS Dilini Seçin:",
        "select_voice": "Ses Seçin:",
        "selected_voice_info": "Seçilen Ses Bilgisi:",
        "voice_id_label": "Ses Kimliği",
        "engine_label": "Motor",
        "language_label": "Dil",
        "gender_label": "Cinsiyet",
        "enter_text_header": "Metni Girin",
        "text_area_label": "Sese dönüştürülecek metni buraya yazın:",
        "text_area_placeholder": "Merhaba! Amazon Polly kullanarak metinden sese dönüştürme uygulamasına hoş geldiniz.",
        "generate_audio_button": "🎧 Sesi Oluştur",
        "generating_audio_spinner": "{voice_name} sesiyle metin sese dönüştürülüyor...",
        "audio_success": "✔️ Ses başarıyla oluşturuldu!",
        "audio_error": "❌ Ses oluşturulamadı. Lütfen yukarıdaki hata mesajlarını kontrol edin.",
        "no_text_warning": "⚠️ Lütfen sese dönüştürmek için bir metin girin.",
        "polly_client_error_config": "Polly istemcisi başlatılamadı. Lütfen AWS kimlik bilgilerinin (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION) Streamlit Secrets veya ortam değişkenlerinde doğru şekilde ayarlandığından emin olun.",
        "polly_client_error_runtime": "Polly istemcisi mevcut değil. Lütfen AWS yapılandırmasını kontrol edin.",
        "polly_api_error": "Amazon Polly API hatası: {error}",
        "unknown_synthesis_error": "Ses sentezlenirken bilinmeyen bir hata oluştu: {error}",
        "no_audio_stream": "Polly'den ses akışı alınamadı.",
        "generated_audio_header": "Oluşturulan Ses",
        "download_mp3_button": "🎵 MP3 Olarak İndir",
        "developer_info_header": "🧑‍💻 Geliştirici",
        "developer_github": "GitHub",
        "developer_linkedin": "LinkedIn",
        "no_voices_for_language": "{language_name} ({language_code}) için kullanılabilir ses bulunamadı.",
        "select_valid_voice_warning": "Lütfen geçerli bir ses seçin.",
        "no_voices_from_polly_warning": "Amazon Polly'den hiçbir ses alınamadı. Lütfen AWS yapılandırmanızı ve Polly servis durumunu kontrol edin."
    }
}

if 'ui_language' not in st.session_state:
    st.session_state.ui_language = "tr"
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None
if 'selected_tts_language_code' not in st.session_state:
    st.session_state.selected_tts_language_code = None
if 'selected_voice_info' not in st.session_state:
    st.session_state.selected_voice_info = None

def t(key, **kwargs):
    lang_code = st.session_state.get('ui_language', 'en')
    return translations.get(lang_code, translations['en']).get(key, f"<{key}>").format(**kwargs)

@st.cache_resource
def get_polly_client():
    aws_access_key_id = None
    aws_secret_access_key = None
    aws_region = None
    if hasattr(st, 'secrets'):
        try:
            aws_access_key_id = st.secrets.get("AWS_ACCESS_KEY_ID")
            aws_secret_access_key = st.secrets.get("AWS_SECRET_ACCESS_KEY")
            aws_region = st.secrets.get("AWS_DEFAULT_REGION")
        except Exception:
            pass
    if not aws_access_key_id:
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    if not aws_secret_access_key:
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    if not aws_region:
        aws_region = os.environ.get('AWS_DEFAULT_REGION')
    if not aws_region:
        aws_region = "us-east-1"
    if not all([aws_access_key_id, aws_secret_access_key, aws_region]):
        return None
    try:
        client = boto3.client(
            'polly',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        return client
    except Exception:
        return None

polly_client = get_polly_client()

@st.cache_data(show_spinner=False)
def get_available_voices(_client_ref):
    if not _client_ref:
        return {}, {}
    all_polly_voices_raw = []
    try:
        paginator = _client_ref.get_paginator('describe_voices')
        for page in paginator.paginate():
            all_polly_voices_raw.extend(page['Voices'])
    except (BotoCoreError, ClientError):
        return {}, {}
    voices_by_lang_code = {}
    lang_code_to_name_map = {}
    for voice_detail in all_polly_voices_raw:
        lang_code = voice_detail['LanguageCode']
        lang_name = voice_detail['LanguageName']
        if lang_code not in voices_by_lang_code:
            voices_by_lang_code[lang_code] = []
            lang_code_to_name_map[lang_code] = lang_name
        for engine in voice_detail['SupportedEngines']:
            voices_by_lang_code[lang_code].append({
                "display_name": f"{voice_detail['Name']} ({engine.capitalize()}) - {voice_detail['Gender']}",
                "id": voice_detail['Id'],
                "engine": engine,
                "gender": voice_detail['Gender'],
                "language_code": lang_code,
                "language_name": lang_name
            })
    sorted_lang_codes = sorted(lang_code_to_name_map.keys(), key=lambda k: (lang_code_to_name_map[k], k))
    sorted_lang_code_to_name_map = {code: lang_code_to_name_map[code] for code in sorted_lang_codes}
    return voices_by_lang_code, sorted_lang_code_to_name_map

def synthesize_speech(client, text, voice_id, engine):
    if not client:
        st.error(t("polly_client_error_runtime"))
        return None, None
    try:
        response = client.synthesize_speech(
            Text=text, OutputFormat="mp3", VoiceId=voice_id, Engine=engine
        )
    except (BotoCoreError, ClientError) as error:
        st.error(t("polly_api_error", error=error))
        return None, None
    except Exception as e:
        st.error(t("unknown_synthesis_error", error=e))
        return None, None
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            return stream.read(), "audio/mpeg"
    else:
        st.error(t("no_audio_stream"))
        return None, None

st.title(t("app_main_title"))
st.markdown(t("app_description"))
st.markdown("---")

if not polly_client:
    st.error(t("polly_client_error_config"))
    st.stop()

ALL_VOICES_BY_LANG_CODE, LANG_CODE_TO_NAME_MAP = get_available_voices(polly_client)
if not ALL_VOICES_BY_LANG_CODE:
    st.warning(t("no_voices_from_polly_warning"))

st.sidebar.header(t("settings_header"))

available_ui_langs_map = {"Türkçe": "tr", "English": "en"}
current_ui_lang_display_name = [name for name, code in available_ui_langs_map.items() if code == st.session_state.ui_language][0]
selected_ui_lang_display_name = st.sidebar.selectbox(
    label=t("select_ui_language"),
    options=list(available_ui_langs_map.keys()),
    index=list(available_ui_langs_map.keys()).index(current_ui_lang_display_name)
)
selected_ui_lang_code = available_ui_langs_map[selected_ui_lang_display_name]
if st.session_state.ui_language != selected_ui_lang_code:
    st.session_state.ui_language = selected_ui_lang_code
    st.rerun()

tts_language_display_options = {f"{name} ({code})": code for code, name in LANG_CODE_TO_NAME_MAP.items()}
if st.session_state.selected_tts_language_code not in tts_language_display_options.values():
    st.session_state.selected_tts_language_code = next(iter(tts_language_display_options.values()), None)

current_selected_tts_lang_display = None
if st.session_state.selected_tts_language_code:
    for display, code in tts_language_display_options.items():
        if code == st.session_state.selected_tts_language_code:
            current_selected_tts_lang_display = display
            break
selected_tts_lang_display = st.sidebar.selectbox(
    label=t("select_voice_language"),
    options=list(tts_language_display_options.keys()),
    index=list(tts_language_display_options.keys()).index(current_selected_tts_lang_display) if current_selected_tts_lang_display else 0,
    disabled=not tts_language_display_options
)
if selected_tts_lang_display:
    st.session_state.selected_tts_language_code = tts_language_display_options[selected_tts_lang_display]
else:
    st.session_state.selected_tts_language_code = None

voices_for_selected_lang_list = []
if st.session_state.selected_tts_language_code:
    voices_for_selected_lang_list = ALL_VOICES_BY_LANG_CODE.get(st.session_state.selected_tts_language_code, [])
voice_display_options = {voice['display_name']: voice for voice in voices_for_selected_lang_list}

if voice_display_options:
    current_selected_voice_display_name = None
    if st.session_state.selected_voice_info and st.session_state.selected_voice_info['display_name'] in voice_display_options:
        current_selected_voice_display_name = st.session_state.selected_voice_info['display_name']
    elif voice_display_options:
        current_selected_voice_display_name = next(iter(voice_display_options.keys()))
    selected_voice_display_name = st.sidebar.selectbox(
        label=t("select_voice"),
        options=list(voice_display_options.keys()),
        index=list(voice_display_options.keys()).index(current_selected_voice_display_name) if current_selected_voice_display_name else 0
    )
    st.session_state.selected_voice_info = voice_display_options[selected_voice_display_name]
    st.sidebar.markdown(f"**{t('selected_voice_info')}**")
    st.sidebar.markdown(f"- **{t('voice_id_label')}:** `{st.session_state.selected_voice_info['id']}`")
    st.sidebar.markdown(f"- **{t('engine_label')}:** `{st.session_state.selected_voice_info['engine'].capitalize()}`")
    st.sidebar.markdown(f"- **{t('language_label')}:** `{st.session_state.selected_voice_info['language_name']}`")
    st.sidebar.markdown(f"- **{t('gender_label')}:** `{st.session_state.selected_voice_info['gender']}`")
elif st.session_state.selected_tts_language_code:
    lang_name_for_warning = LANG_CODE_TO_NAME_MAP.get(st.session_state.selected_tts_language_code, st.session_state.selected_tts_language_code)
    st.sidebar.warning(t("no_voices_for_language", language_name=lang_name_for_warning, language_code=st.session_state.selected_tts_language_code))
    st.session_state.selected_voice_info = None
else:
    st.session_state.selected_voice_info = None

st.subheader(t("enter_text_header"))
text_to_convert = st.text_area(
    label=t("text_area_label"), height=200, placeholder=t("text_area_placeholder")
)
generate_button_disabled = not st.session_state.selected_voice_info
if st.button(t("generate_audio_button"), type="primary", use_container_width=True, disabled=generate_button_disabled):
    if not text_to_convert:
        st.warning(t("no_text_warning"))
    elif not st.session_state.selected_voice_info:
        st.warning(t("select_valid_voice_warning"))
    else:
        voice_id = st.session_state.selected_voice_info['id']
        engine = st.session_state.selected_voice_info['engine']
        voice_name_for_spinner = st.session_state.selected_voice_info['display_name'].split(' (')[0]
        with st.spinner(t("generating_audio_spinner", voice_name=voice_name_for_spinner)):
            audio_bytes, mime_type = synthesize_speech(polly_client, text_to_convert, voice_id, engine)
            if audio_bytes:
                st.session_state.audio_bytes = audio_bytes
                clean_voice_id = "".join(c if c.isalnum() else "_" for c in voice_id)
                st.session_state.file_name = f"polly_tts_{clean_voice_id}.mp3"
                st.success(t("audio_success"))
            else:
                st.session_state.audio_bytes = None

if st.session_state.audio_bytes:
    st.subheader(t("generated_audio_header"))
    st.audio(st.session_state.audio_bytes, format="audio/mpeg")
    st.download_button(
        label=t("download_mp3_button"),
        data=st.session_state.audio_bytes,
        file_name=st.session_state.file_name,
        mime="audio/mpeg",
        use_container_width=True
    )

st.sidebar.markdown("---")
st.sidebar.subheader(t("developer_info_header"))
st.sidebar.markdown(f"[{t('developer_github')}](https://github.com/keremalagoz) | [{t('developer_linkedin')}](https://www.linkedin.com/in/keremalagoz/)")
