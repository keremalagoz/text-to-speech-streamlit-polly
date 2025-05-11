import streamlit as st
import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from dotenv import load_dotenv # .env dosyasını yüklemek için

# Ortam değişkenlerini .env dosyasından yükle (eğer varsa)
# Bu satır, lokalde .env dosyası kullanıyorsanız AWS kimlik bilgilerini yükler.
# Streamlit Cloud'da secrets yönetimi farklıdır.
load_dotenv()

# --- AWS Polly İstemcisini Yapılandırma ---

def get_polly_client():
    """AWS Polly istemcisini başlatır."""
    try:
        # 1. Streamlit secrets'tan (Streamlit Cloud için)
        aws_access_key_id = st.secrets.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = st.secrets.get("AWS_SECRET_ACCESS_KEY")
        aws_region = st.secrets.get("AWS_DEFAULT_REGION", "eu-west-1")
    except AttributeError:
        # st.secrets yoksa (lokalde veya secrets tanımlanmamışsa)
        aws_access_key_id = None
        aws_secret_access_key = None
        aws_region = "eu-west-1" # Varsayılan

    # 2. Ortam değişkenlerinden (lokal .env veya sistem ortam değişkenleri)
    if not all([aws_access_key_id, aws_secret_access_key]):
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        # Bölge için ortam değişkeni varsa onu kullan, yoksa varsayılanı koru
        aws_region_env = os.environ.get('AWS_DEFAULT_REGION')
        if aws_region_env:
            aws_region = aws_region_env


    if not all([aws_access_key_id, aws_secret_access_key, aws_region]):
        st.error("AWS kimlik bilgileri (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION) bulunamadı. Lütfen Streamlit secrets veya ortam değişkenleri ile ayarlayın.")
        return None

    try:
        client = boto3.client(
            'polly',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        return client
    except Exception as e:
        st.error(f"AWS Polly istemcisi başlatılırken hata oluştu: {e}")
        return None

polly_client = get_polly_client()

# --- Metin Okuma Fonksiyonu ---
def synthesize_speech(client, text, voice_id, engine="standard"):
    """
    Verilen metni Amazon Polly kullanarak ses dosyasına dönüştürür.
    """
    if not client:
        st.error("Polly istemcisi düzgün başlatılamadı. Lütfen AWS ayarlarınızı kontrol edin.")
        return None, None

    try:
        response = client.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId=voice_id,
            Engine=engine
        )
    except (BotoCoreError, ClientError) as error:
        st.error(f"Amazon Polly API hatası: {error}")
        return None, None
    except Exception as e:
        st.error(f"Ses sentezlenirken bilinmeyen bir hata oluştu: {e}")
        return None, None

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            audio_bytes = stream.read()
            return audio_bytes, "audio/mpeg"  # MP3 için MIME type
    else:
        st.error("Polly'den ses akışı alınamadı.")
        return None, None

# --- Streamlit Arayüzü ---
st.set_page_config(page_title="Metin Okuma (TTS) Uygulaması", layout="wide", initial_sidebar_state="expanded")

st.title("🎙️ Amazon Polly ile Metin Okuma (TTS)")
st.markdown("Bu uygulama, girdiğiniz metni Amazon Polly servisini kullanarak sese dönüştürür.")
st.markdown("---")

# Kullanılabilir sesler (Türkçe)
# Format: "Görünen Ad": (VoiceId, Motor)
available_voices_tr = {
    "Filiz (Standart Kadın)": ("Filiz", "standard"),
    "Zehra (Nöral Kadın)": ("Zehra", "neural"),
    # Diğer diller ve sesler için Polly dokümantasyonuna bakın ve buraya ekleyebilirsiniz.
}
# Örnek İngilizce sesler:
# available_voices_en = {
#     "Joanna (Nöral Kadın - EN)": ("Joanna", "neural"),
#     "Matthew (Nöral Erkek - EN)": ("Matthew", "neural"),
# }
# all_voices = {**available_voices_tr, **available_voices_en}


st.sidebar.header("⚙️ Ayarlar")
selected_voice_display_name = st.sidebar.selectbox(
    "Bir Ses Seçin:",
    options=list(available_voices_tr.keys()),
    help="Kullanmak istediğiniz sesi seçin. 'Nöral' sesler daha doğal ve akıcıdır."
)

voice_id, engine = available_voices_tr[selected_voice_display_name]

st.sidebar.info(f"""
    **Seçilen Ses:**
    - Ad: `{selected_voice_display_name.split(' (')[0]}`
    - Voice ID: `{voice_id}`
    - Motor: `{engine.capitalize()}`
    """)

st.subheader("Metni Girin")
text_to_convert = st.text_area(
    "Sese dönüştürülecek metni buraya yazın:",
    height=250,
    placeholder="Merhaba! Amazon Polly kullanarak metinden sese dönüştürme uygulamasına hoş geldiniz."
)

# Session state'i kullanarak ses verisini ve indirme durumunu saklayalım
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None


if st.button("🎧 Sesi Oluştur", type="primary", use_container_width=True, disabled=not polly_client):
    if text_to_convert:
        if not polly_client:
            st.error("Lütfen önce AWS kimlik bilgilerini doğru şekilde yapılandırın ve sayfayı yenileyin.")
        else:
            with st.spinner(f"`{selected_voice_display_name.split(' (')[0]}` sesiyle metin sese dönüştürülüyor..."):
                audio_bytes, mime_type = synthesize_speech(polly_client, text_to_convert, voice_id, engine)

                if audio_bytes:
                    st.session_state.audio_bytes = audio_bytes
                    st.session_state.file_name = f"polly_output_{voice_id.lower().replace(' ', '_')}.mp3"
                    st.success("✔️ Ses başarıyla oluşturuldu!")
                else:
                    st.session_state.audio_bytes = None # Başarısız olursa temizle
                    st.error("❌ Ses oluşturulamadı. Lütfen yukarıdaki hata mesajlarını kontrol edin.")
    else:
        st.warning("⚠️ Lütfen sese dönüştürmek için bir metin girin.")

# Oluşturulan sesi göster ve indirme butonu ekle
if st.session_state.audio_bytes:
    st.subheader("Oluşturulan Ses")
    st.audio(st.session_state.audio_bytes, format="audio/mpeg")
    st.download_button(
        label="🎵 MP3 Olarak İndir",
        data=st.session_state.audio_bytes,
        file_name=st.session_state.file_name,
        mime="audio/mpeg",
        use_container_width=True
    )

st.markdown("---")
st.sidebar.markdown("---")
st.sidebar.subheader("💡 Bilgilendirme")
st.sidebar.info("""
- Amazon Polly, AWS Ücretsiz Kullanım Katmanı kapsamında 12 ay boyunca ücretsizdir:
    - **Standart Sesler:** Ayda 5 milyon karakter.
    - **Nöral Sesler (NTTS):** Ayda 1 milyon karakter.
- Bu limitleri aşarsanız veya 12 ay dolduktan sonra standart ücretlendirme uygulanır.
- Kullanımınızı [AWS Billing Dashboard](https://console.aws.amazon.com/billing/) üzerinden takip edebilirsiniz.
""")
st.sidebar.markdown("Geliştiren: [Adınız / GitHub Kullanıcı Adınız]") # Kendi bilgilerinizi ekleyin