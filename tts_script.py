import streamlit as st
import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from dotenv import load_dotenv

# Ortam değişkenlerini .env dosyasından yükle (eğer varsa)
load_dotenv()

# --- Dil Çevirileri ---
# Uygulama arayüzü için dil çevirilerini burada tanımlayacağız.
# İhtiyaç duydukça yeni diller ve çeviriler ekleyebilirsiniz.
translations = {
    "en": {
        "app_title": "🎙️ Text-to-Speech (TTS) with Amazon Polly",
        "app_description": "This application converts your input text into speech using Amazon Polly.",
        "settings_header": "⚙️ Settings",
        "select_ui_language": "Select UI Language:",
        "select_voice_language": "Select TTS Language:",
        "select_voice": "Select Voice:",
        "selected_voice_info": "Selected Voice Info:",
        "voice_id_label": "Voice ID",
        "engine_label": "Engine",
        "language_label": "Language",
        "enter_text_header": "Enter Text",
        "text_area_label": "Enter text to convert to speech here:",
        "text_area_placeholder": "Hello! Welcome to the text-to-speech application using Amazon Polly.",
        "generate_audio_button": "🎧 Generate Audio",
        "generating_audio_spinner": "Converting text to speech with {voice_name}...",
        "audio_success": "✔️ Audio successfully generated!",
        "audio_error": "❌ Audio could not be generated. Please check error messages above.",
        "no_text_warning": "⚠️ Please enter some text to convert.",
        "polly_client_error": "Polly client could not be initialized. Please check your AWS settings.",
        "polly_api_error": "Amazon Polly API error: {error}",
        "unknown_synthesis_error": "An unknown error occurred during speech synthesis: {error}",
        "no_audio_stream": "Could not retrieve audio stream from Polly.",
        "generated_audio_header": "Generated Audio",
        "download_mp3_button": "🎵 Download as MP3",
        "aws_free_tier_info_header": "💡 Information",
        "aws_free_tier_info_text": """
- Amazon Polly is free for 12 months under the AWS Free Tier:
    - **Standard Voices:** 5 million characters per month.
    - **Neural Voices (NTTS):** 1 million characters per month.
- Standard pricing applies if you exceed these limits or after 12 months.
- Track your usage via the [AWS Billing Dashboard](https://console.aws.amazon.com/billing/).
""",
        "developer_info": "Developed by: [Your Name / GitHub Username]" # Kendi bilgilerinizi ekleyin
    },
    "tr": {
        "app_title": "🎙️ Amazon Polly ile Metin Okuma (TTS)",
        "app_description": "Bu uygulama, girdiğiniz metni Amazon Polly servisini kullanarak sese dönüştürür.",
        "settings_header": "⚙️ Ayarlar",
        "select_ui_language": "Arayüz Dilini Seçin:",
        "select_voice_language": "TTS Dilini Seçin:",
        "select_voice": "Ses Seçin:",
        "selected_voice_info": "Seçilen Ses Bilgisi:",
        "voice_id_label": "Ses Kimliği",
        "engine_label": "Motor",
        "language_label": "Dil",
        "enter_text_header": "Metni Girin",
        "text_area_label": "Sese dönüştürülecek metni buraya yazın:",
        "text_area_placeholder": "Merhaba! Amazon Polly kullanarak metinden sese dönüştürme uygulamasına hoş geldiniz.",
        "generate_audio_button": "🎧 Sesi Oluştur",
        "generating_audio_spinner": "{voice_name} sesiyle metin sese dönüştürülüyor...",
        "audio_success": "✔️ Ses başarıyla oluşturuldu!",
        "audio_error": "❌ Ses oluşturulamadı. Lütfen yukarıdaki hata mesajlarını kontrol edin.",
        "no_text_warning": "⚠️ Lütfen sese dönüştürmek için bir metin girin.",
        "polly_client_error": "Polly istemcisi başlatılamadı. Lütfen AWS ayarlarınızı kontrol edin.",
        "polly_api_error": "Amazon Polly API hatası: {error}",
        "unknown_synthesis_error": "Ses sentezlenirken bilinmeyen bir hata oluştu: {error}",
        "no_audio_stream": "Polly'den ses akışı alınamadı.",
        "generated_audio_header": "Oluşturulan Ses",
        "download_mp3_button": "🎵 MP3 Olarak İndir",
        "aws_free_tier_info_header": "💡 Bilgilendirme",
        "aws_free_tier_info_text": """
- Amazon Polly, AWS Ücretsiz Kullanım Katmanı kapsamında 12 ay boyunca ücretsizdir:
    - **Standart Sesler:** Ayda 5 milyon karakter.
    - **Nöral Sesler (NTTS):** Ayda 1 milyon karakter.
- Bu limitleri aşarsanız veya 12 ay dolduktan sonra standart ücretlendirme uygulanır.
- Kullanımınızı [AWS Billing Dashboard](https://console.aws.amazon.com/billing/) üzerinden takip edebilirsiniz.
""",
        "developer_info": "Geliştiren: [Kerem Alagöz / keremalagoz" 
    }
}

# --- AWS Polly İstemcisini Yapılandırma ---
@st.cache_resource # Kaynağı önbellekle, tekrar tekrar client oluşturma
def get_polly_client():
    """AWS Polly istemcisini başlatır."""
    try:
        aws_access_key_id = st.secrets.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = st.secrets.get("AWS_SECRET_ACCESS_KEY")
        aws_region = st.secrets.get("AWS_DEFAULT_REGION", "us-east-1") # Polly'nin olduğu bir bölge
    except AttributeError: # st.secrets yoksa (lokal test)
        aws_access_key_id = None
        aws_secret_access_key = None
        aws_region = "us-east-1"

    if not all([aws_access_key_id, aws_secret_access_key]):
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region_env = os.environ.get('AWS_DEFAULT_REGION')
        if aws_region_env:
            aws_region = aws_region_env

    if not all([aws_access_key_id, aws_secret_access_key, aws_region]):
        # Hata mesajını UI dili seçildikten sonra göstermek daha iyi olabilir.
        # Şimdilik, client None dönecek ve bu aşağıda ele alınacak.
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

# --- Polly Seslerini Getirme Fonksiyonu ---
@st.cache_data(show_spinner=False) # Veriyi önbellekle
def get_available_voices(_client): # _client parametresi cache'in client değiştiğinde yenilenmesi için
    """Amazon Polly'den kullanılabilir tüm sesleri ve dilleri alır."""
    if not _client:
        return {}, {} # voices_by_lang, lang_names

    all_voices = []
    try:
        paginator = _client.get_paginator('describe_voices')
        for page in paginator.paginate():
            all_voices.extend(page['Voices'])
    except (BotoCoreError, ClientError) as error:
        st.error(f"Polly sesleri alınırken hata: {error}")
        return {}, {}

    voices_by_lang = {}
    lang_names = {} # Dil kodlarını dil adlarına eşlemek için (örn: tr-TR -> Turkish)

    for voice in all_voices:
        lang_code = voice['LanguageCode']
        lang_name = voice['LanguageName']
        if lang_code not in voices_by_lang:
            voices_by_lang[lang_code] = []
            lang_names[lang_code] = lang_name

        # Her ses için birden fazla motor olabilir, bunları ayrı seçenekler olarak sunalım
        for engine in voice['SupportedEngines']:
            display_name = f"{voice['Name']} ({engine.capitalize()})"
            voices_by_lang[lang_code].append({
                "display_name": display_name,
                "id": voice['Id'],
                "engine": engine,
                "gender": voice['Gender']
            })
    # Dilleri alfabetik olarak sırala
    sorted_lang_codes = sorted(lang_names.keys(), key=lambda k: lang_names[k])
    sorted_lang_names = {code: lang_names[code] for code in sorted_lang_codes}

    return voices_by_lang, sorted_lang_names

# --- Metin Okuma Fonksiyonu ---
def synthesize_speech(client, text, voice_id, engine):
    """Verilen metni Amazon Polly kullanarak ses dosyasına dönüştürür."""
    ui_lang = st.session_state.get('ui_language', 'en')
    if not client:
        st.error(translations[ui_lang]["polly_client_error"])
        return None, None

    try:
        response = client.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId=voice_id,
            Engine=engine
        )
    except (BotoCoreError, ClientError) as error:
        st.error(translations[ui_lang]["polly_api_error"].format(error=error))
        return None, None
    except Exception as e:
        st.error(translations[ui_lang]["unknown_synthesis_error"].format(error=e))
        return None, None

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            audio_bytes = stream.read()
            return audio_bytes, "audio/mpeg"
    else:
        st.error(translations[ui_lang]["no_audio_stream"])
        return None, None

# --- Streamlit Arayüzü ---

# Session state başlatma
if 'ui_language' not in st.session_state:
    st.session_state.ui_language = "tr" # Varsayılan arayüz dili Türkçe
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None
if 'selected_tts_language' not in st.session_state:
    st.session_state.selected_tts_language = None
if 'selected_voice_info' not in st.session_state:
    st.session_state.selected_voice_info = None


# UI dilini almak için yardımcı fonksiyon
def t(key, **kwargs):
    return translations[st.session_state.ui_language].get(key, key).format(**kwargs)

# Sayfa Yapılandırması (Dil seçimi değiştiğinde yeniden çalıştırılır)
st.set_page_config(page_title=t("app_title"), layout="wide", initial_sidebar_state="expanded")
st.title(t("app_title"))
st.markdown(t("app_description"))
st.markdown("---")

if not polly_client:
    st.error(t("polly_client_error") + " " + "Lütfen AWS kimlik bilgilerinizi Streamlit Secrets veya ortam değişkenleri ile doğru şekilde ayarladığınızdan emin olun.")
    st.stop() # Polly client yoksa uygulamayı durdur

# Polly seslerini ve dillerini al
VOICES_BY_LANG, LANG_NAMES = get_available_voices(polly_client)

if not VOICES_BY_LANG:
    st.warning("Amazon Polly'den hiçbir ses alınamadı. Lütfen AWS yapılandırmanızı ve Polly servis durumunu kontrol edin.")
    st.stop()

# --- Kenar Çubuğu (Sidebar) ---
st.sidebar.header(t("settings_header"))

# Arayüz Dili Seçimi
available_ui_langs = {"Türkçe": "tr", "English": "en"} # Daha fazla dil ekleyebilirsiniz
selected_ui_lang_display = st.sidebar.selectbox(
    label=t("select_ui_language"), # Bu label ilk başta varsayılan dilde olacak
    options=available_ui_langs.keys(),
    index=list(available_ui_langs.values()).index(st.session_state.ui_language), # Mevcut seçimi koru
    key="ui_language_selector_key" # Yeniden render için benzersiz anahtar
)
# Seçilen UI dilini session state'e ata
# Bu atama, sayfanın yeniden çalışmasını tetikleyebilir ve tüm metinler güncellenir.
if st.session_state.ui_language != available_ui_langs[selected_ui_lang_display]:
    st.session_state.ui_language = available_ui_langs[selected_ui_lang_display]
    st.experimental_rerun() # Arayüz dilini anında güncellemek için

# TTS Dili Seçimi
# LANG_NAMES: {'en-US': 'US English', 'tr-TR': 'Turkish', ...}
# Options için dil adlarını ve kodlarını birleştirerek daha kullanıcı dostu yapalım
tts_language_options = {f"{name} ({code})": code for code, name in LANG_NAMES.items()}

# Eğer daha önce bir dil seçilmemişse veya seçilen dil artık mevcut değilse, varsayılanı ayarla
if st.session_state.selected_tts_language not in tts_language_options.values():
    st.session_state.selected_tts_language = next(iter(tts_language_options.values()), None) # İlk uygun dili al

selected_tts_lang_display = st.sidebar.selectbox(
    label=t("select_voice_language"),
    options=list(tts_language_options.keys()),
    index=list(tts_language_options.values()).index(st.session_state.selected_tts_language)
            if st.session_state.selected_tts_language in tts_language_options.values() else 0,
    key="tts_language_selector_key"
)
st.session_state.selected_tts_language = tts_language_options[selected_tts_lang_display]


# Seçilen dile ait sesleri al
voices_for_selected_lang = VOICES_BY_LANG.get(st.session_state.selected_tts_language, [])
voice_options = {voice['display_name']: voice for voice in voices_for_selected_lang}

# Eğer sesler varsa devam et
if voice_options:
    # Eğer daha önce bir ses seçilmemişse veya seçilen ses artık mevcut değilse, varsayılanı ayarla
    current_selected_voice_display = st.session_state.get("selected_voice_display_name")
    if current_selected_voice_display not in voice_options:
        current_selected_voice_display = next(iter(voice_options.keys()), None)

    selected_voice_display_name = st.sidebar.selectbox(
        label=t("select_voice"),
        options=list(voice_options.keys()),
        index=list(voice_options.keys()).index(current_selected_voice_display) if current_selected_voice_display else 0,
        key="voice_selector_key"
    )
    st.session_state.selected_voice_display_name = selected_voice_display_name
    st.session_state.selected_voice_info = voice_options[selected_voice_display_name]

    # Seçilen ses bilgilerini göster
    st.sidebar.markdown(f"**{t('selected_voice_info')}**")
    st.sidebar.json({
        t("voice_id_label"): st.session_state.selected_voice_info['id'],
        t("engine_label"): st.session_state.selected_voice_info['engine'].capitalize(),
        t("language_label"): LANG_NAMES[st.session_state.selected_tts_language]
    })
else:
    st.sidebar.warning(f"{LANG_NAMES.get(st.session_state.selected_tts_language, st.session_state.selected_tts_language)} için kullanılabilir ses bulunamadı.")
    st.session_state.selected_voice_info = None # Ses yoksa bilgiyi temizle


# --- Ana İçerik ---
st.subheader(t("enter_text_header"))
text_to_convert = st.text_area(
    label=t("text_area_label"),
    height=200,
    placeholder=t("text_area_placeholder")
)

if st.button(t("generate_audio_button"), type="primary", use_container_width=True, disabled=not st.session_state.selected_voice_info):
    if text_to_convert and st.session_state.selected_voice_info:
        voice_id = st.session_state.selected_voice_info['id']
        engine = st.session_state.selected_voice_info['engine']
        voice_name_for_spinner = st.session_state.selected_voice_info['display_name'].split(' (')[0]

        with st.spinner(t("generating_audio_spinner", voice_name=voice_name_for_spinner)):
            audio_bytes, mime_type = synthesize_speech(polly_client, text_to_convert, voice_id, engine)

            if audio_bytes:
                st.session_state.audio_bytes = audio_bytes
                st.session_state.file_name = f"polly_tts_{voice_id.lower().replace(' ', '_')}.mp3"
                st.success(t("audio_success"))
            else:
                st.session_state.audio_bytes = None
                # Hata mesajı synthesize_speech içinde zaten gösterildi.
    elif not st.session_state.selected_voice_info:
        st.warning(t("Lütfen geçerli bir ses seçin.")) # Bu mesajı da çeviri dosyasına ekleyebilirsiniz.
    else:
        st.warning(t("no_text_warning"))

# Oluşturulan sesi göster ve indirme butonu ekle
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

# Bilgilendirme
st.sidebar.markdown("---")
st.sidebar.subheader(t("aws_free_tier_info_header"))
st.sidebar.markdown(t("aws_free_tier_info_text"), unsafe_allow_html=True)
st.sidebar.markdown(t("developer_info"))
