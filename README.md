# Text-to-Speech (TTS) with Amazon Polly - Streamlit App / Amazon Polly ile Metin Okuma (TTS) - Streamlit Uygulaması

This is an interactive web application built with [Streamlit](https://streamlit.io/) and Amazon Web Services (AWS) [Polly](https://aws.amazon.com/polly/) that converts text into natural-sounding speech. / Bu, [Streamlit](https://streamlit.io/) ve Amazon Web Services (AWS) [Polly](https://aws.amazon.com/polly/) servisleri kullanılarak metni doğal sondajlı sese dönüştüren interaktif bir web uygulamasıdır.

🌐 **[View Live Demo (if deployed) / Canlı Demoyu Görüntüle (Eğer Dağıtıldıysa)](YOUR_STREAMLIT_APP_URL_HERE)**  _(Replace with your actual app URL / Gerçek uygulama URL'niz ile değiştirin)_

---

**Languages / Diller:**
*   [English Description](#english-description)
*   [Türkçe Açıklama](#türkçe-açıklama)

---

## English Description

### Features

*   Convert user-input text to speech.
*   Select from a wide range of Amazon Polly voices across multiple languages and regions.
*   Choose between standard and neural (NTTS) voices for higher quality.
*   Listen to the generated audio directly in the browser.
*   Download the generated audio as an MP3 file.
*   User interface available in English and Turkish.
*   Responsive design, usable on mobile and desktop devices.

### Screenshots

_(Add a screenshot of your application here. You can drag and drop an image into the GitHub editor or use Markdown's image syntax: ![App Screenshot](path/to/your/screenshot.png))_

### Setup and Running

#### Prerequisites

*   Python 3.8 or higher.
*   An AWS Account.
*   An IAM user with programmatic access and permissions to use the Amazon Polly service (e.g., `AmazonPollyReadOnlyAccess` or `AmazonPollyFullAccess`). You will need the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` for this user.
*   Your preferred AWS Region where Polly is available (e.g., `us-east-1`, `eu-west-1`). This will be your `AWS_DEFAULT_REGION`.

#### Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/keremalagoz/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```
    _(Replace `YOUR_REPOSITORY_NAME` with your actual repository name)_

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure AWS Credentials:**

    The application needs your AWS credentials to access Amazon Polly. You can set them up in one of the following ways:

    *   **For Streamlit Community Cloud Deployment (Recommended):**
        Add your credentials as "Secrets" in your app's settings:
        *   `AWS_ACCESS_KEY_ID` = "YOUR_AWS_ACCESS_KEY_ID"
        *   `AWS_SECRET_ACCESS_KEY` = "YOUR_AWS_SECRET_ACCESS_KEY"
        *   `AWS_DEFAULT_REGION` = "YOUR_AWS_REGION" (e.g., `us-east-1`)

    *   **For Local Development - `.streamlit/secrets.toml` File:**
        Create a folder named `.streamlit` in the project root. Inside it, create a file named `secrets.toml`:
        ```toml
        # .streamlit/secrets.toml
        AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY_ID_HERE"
        AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY_HERE"
        AWS_DEFAULT_REGION = "us-east-1"
        ```
        **IMPORTANT:** DO NOT COMMIT THIS FILE TO GITHUB! Ensure it's in your `.gitignore`.

    *   **For Local Development - `.env` File:**
        Create a `.env` file in the project root:
        ```env
        # .env
        AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID_HERE"
        AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY_HERE"
        AWS_DEFAULT_REGION="us-east-1"
        ```
        **IMPORTANT:** DO NOT COMMIT THIS FILE TO GITHUB! Ensure it's in your `.gitignore`.

    *   **System Environment Variables:** You can also set your credentials as system environment variables.

5.  **Run the Streamlit Application:**
    ```bash
    streamlit run app.py
    ```
    The application will typically open at `http://localhost:8501`.

### How to Use

1.  Select your preferred UI language (English/Turkish) from the sidebar.
2.  Choose the desired TTS language from the "Select TTS Language" dropdown.
3.  Select a specific voice (standard or neural) from the "Select Voice" dropdown.
4.  Enter or paste the text into the text area.
5.  Click the "Generate Audio" button.
6.  The audio will be generated and played. A "Download as MP3" button will appear.

### About Amazon Polly

Amazon Polly is a service that turns text into lifelike speech. For new AWS accounts, Polly is included in the AWS Free Tier for 12 months, with certain usage limits. If you exceed these limits or after the 12-month period, standard [Amazon Polly pricing](https://aws.amazon.com/polly/pricing/) will apply.

### Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/keremalagoz/YOUR_REPOSITORY_NAME/issues).

### License

This project is licensed under the MIT License - see the `LICENSE` file for details (if you add one).

---

<a id="türkçe-açıklama"></a>
## Türkçe Açıklama

### Özellikler

*   Kullanıcı tarafından girilen metni sese dönüştürme.
*   Birden fazla dil ve bölgede geniş bir Amazon Polly ses yelpazesinden seçim yapabilme.
*   Daha yüksek kalite için standart ve nöral (NTTS) sesler arasında seçim yapabilme.
*   Oluşturulan sesi doğrudan tarayıcıda dinleyebilme.
*   Oluşturulan sesi MP3 dosyası olarak indirebilme.
*   İngilizce ve Türkçe dillerinde kullanıcı arayüzü.
*   Mobil ve masaüstü cihazlarda kullanılabilir duyarlı tasarım.

### Ekran Görüntüleri

_(Uygulamanızın bir ekran görüntüsünü buraya ekleyin.)_

### Kurulum ve Çalıştırma

#### Ön Gereksinimler

*   Python 3.8 veya üzeri.
*   Bir AWS Hesabı.
*   Amazon Polly servisini kullanma yetkisine sahip (örn: `AmazonPollyReadOnlyAccess` veya `AmazonPollyFullAccess`) programatik erişime sahip bir IAM kullanıcısı. Bu kullanıcı için `AWS_ACCESS_KEY_ID` ve `AWS_SECRET_ACCESS_KEY` bilgilerine ihtiyacınız olacaktır.
*   Polly'nin mevcut olduğu tercih ettiğiniz AWS Bölgesi (örn: `us-east-1`, `eu-west-1`). Bu, `AWS_DEFAULT_REGION` değeriniz olacaktır.

#### Adımlar

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/keremalagoz/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```
    _(`YOUR_REPOSITORY_NAME` kısmını kendi depo adınızla değiştirin)_

2.  **Sanal Ortam Oluşturun ve Aktifleştirin (Önerilir):**
    ```bash
    python -m venv venv
    # Windows için:
    # venv\Scripts\activate
    # macOS/Linux için:
    # source venv/bin/activate
    ```

3.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **AWS Kimlik Bilgilerini Yapılandırın:**

    Uygulamanın Amazon Polly'ye erişebilmesi için AWS kimlik bilgilerinizin ayarlanması gerekir:

    *   **Streamlit Community Cloud Dağıtımı İçin (Önerilir):**
        Kimlik bilgilerinizi uygulamanızın ayarlarındaki "Secrets" bölümüne ekleyin:
        *   `AWS_ACCESS_KEY_ID` = "SENIN_AWS_ACCESS_KEY_ID"
        *   `AWS_SECRET_ACCESS_KEY` = "SENIN_AWS_SECRET_ACCESS_KEY"
        *   `AWS_DEFAULT_REGION` = "SENIN_AWS_BOLGEN" (örn: `us-east-1`)

    *   **Yerel Geliştirme - `.streamlit/secrets.toml` Dosyası:**
        Proje kök dizininde `.streamlit` klasörü oluşturun. İçine `secrets.toml` dosyası oluşturun:
        ```toml
        # .streamlit/secrets.toml
        AWS_ACCESS_KEY_ID = "SENIN_AWS_ACCESS_KEY_ID_BURAYA"
        AWS_SECRET_ACCESS_KEY = "SENIN_AWS_SECRET_ACCESS_KEY_BURAYA"
        AWS_DEFAULT_REGION = "us-east-1"
        ```
        **ÖNEMLİ:** BU DOSYAYI GITHUB'A YÜKLEMEYİN! `.gitignore` dosyanızda olduğundan emin olun.

    *   **Yerel Geliştirme - `.env` Dosyası:**
        Proje kök dizinine bir `.env` dosyası oluşturun:
        ```env
        # .env
        AWS_ACCESS_KEY_ID="SENIN_AWS_ACCESS_KEY_ID_BURAYA"
        AWS_SECRET_ACCESS_KEY="SENIN_AWS_SECRET_ACCESS_KEY_BURAYA"
        AWS_DEFAULT_REGION="us-east-1"
        ```
        **ÖNEMLİ:** BU DOSYAYI GITHUB'A YÜKLEMEYİN! `.gitignore` dosyanızda olduğundan emin olun.

    *   **Sistem Ortam Değişkenleri:** Kimlik bilgilerinizi sisteminizin ortam değişkenleri olarak da ayarlayabilirsiniz.

5.  **Streamlit Uygulamasını Çalıştırın:**
    ```bash
    streamlit run app.py
    ```
    Uygulama genellikle `http://localhost:8501` adresinde açılacaktır.

### Nasıl Kullanılır?

1.  Kenar çubuğundan tercih ettiğiniz arayüz dilini (Türkçe/İngilizce) seçin.
2.  "TTS Dilini Seçin" açılır menüsünden istediğiniz TTS dilini seçin.
3.  "Ses Seçin" açılır menüsünden belirli bir sesi (standart veya nöral) seçin.
4.  Metin alanına dönüştürmek istediğiniz metni girin veya yapıştırın.
5.  "Sesi Oluştur" düğmesine tıklayın.
6.  Ses oluşturulacak ve çalınacaktır. Bir "MP3 Olarak İndir" düğmesi görünecektir.

### Amazon Polly Hakkında

Amazon Polly, metni canlı gibi konuşmaya dönüştüren bir servistir. Yeni AWS hesapları için Polly, belirli kullanım limitleri dahilinde 12 ay boyunca AWS Ücretsiz Kullanım Katmanı'na dahildir. Bu limitleri aşarsanız veya 12 aylık süre dolduktan sonra standart [Amazon Polly fiyatlandırması](https://aws.amazon.com/polly/pricing/) geçerli olur.

### Katkıda Bulunma

Katkılarınız, sorun bildirimleriniz ve özellik istekleriniz değerlidir! [Sorunlar sayfasına](https://github.com/keremalagoz/YOUR_REPOSITORY_NAME/issues) göz atabilirsiniz.

### Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - ayrıntılar için `LICENSE` dosyasına bakın (eğer eklerseniz).

---

Geliştiren: Kerem Alagöz
*   **GitHub:** [github.com/keremalagoz](https://github.com/keremalagoz)
*   **LinkedIn:** [linkedin.com/in/keremalagoz](https://www.linkedin.com/in/keremalagoz)
