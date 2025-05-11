# Amazon Polly ile Metin Okuma (TTS) - Streamlit Uygulaması

Bu, [Streamlit](https://streamlit.io/) ve Amazon Web Services (AWS) [Polly](https://aws.amazon.com/polly/) servisleri kullanılarak metni doğal sondajlı sese dönüştüren interaktif bir web uygulamasıdır.

🌐 **[Canlı Demoyu Görüntüle (Eğer Dağıtıldıysa)](YOUR_STREAMLIT_APP_URL_HERE)**  _(Gerçek uygulama URL'niz ile değiştirin)_

🇬🇧 **[English Description (İngilizce Açıklama)](README.md)**

## Özellikler

*   Kullanıcı tarafından girilen metni sese dönüştürme.
*   Birden fazla dil ve bölgede geniş bir Amazon Polly ses yelpazesinden seçim yapabilme.
*   Daha yüksek kalite için standart ve nöral (NTTS) sesler arasında seçim yapabilme.
*   Oluşturulan sesi doğrudan tarayıcıda dinleyebilme.
*   Oluşturulan sesi MP3 dosyası olarak indirebilme.
*   İngilizce ve Türkçe dillerinde kullanıcı arayüzü.
*   Mobil ve masaüstü cihazlarda kullanılabilir duyarlı tasarım.

## Ekran Görüntüleri

_(Uygulamanızın bir ekran görüntüsünü buraya ekleyin. GitHub düzenleyicisine bir resim sürükleyip bırakabilir veya Markdown'ın resim sözdizimini kullanabilirsiniz: ![Uygulama Ekran Görüntüsü](path/to/your/screenshot.png))_

## Kurulum ve Çalıştırma

### Ön Gereksinimler

*   Python 3.8 veya üzeri.
*   Bir AWS Hesabı.
*   Amazon Polly servisini kullanma yetkisine sahip (örneğin, `AmazonPollyReadOnlyAccess` veya leksikon gibi özellikleri kullanmayı planlıyorsanız `AmazonPollyFullAccess`) programatik erişime sahip bir IAM kullanıcısı. Bu kullanıcı için `AWS_ACCESS_KEY_ID` ve `AWS_SECRET_ACCESS_KEY` bilgilerine ihtiyacınız olacaktır.
*   Polly'nin mevcut olduğu tercih ettiğiniz AWS Bölgesi (örneğin, `us-east-1`, `eu-west-1`). Bu, `AWS_DEFAULT_REGION` değeriniz olacaktır.

### Adımlar

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

    Uygulamanın Amazon Polly'ye erişebilmesi için AWS kimlik bilgilerinizin ayarlanması gerekir. Aşağıdaki yöntemlerden birini kullanabilirsiniz:

    *   **Streamlit Community Cloud Dağıtımı İçin (Önerilir):**
        Uygulamayı Streamlit Community Cloud'a dağıtıyorsanız, kimlik bilgilerinizi uygulamanızın ayarlarındaki "Secrets" bölümüne ekleyin:
        *   `AWS_ACCESS_KEY_ID` = "SENIN_AWS_ACCESS_KEY_ID"
        *   `AWS_SECRET_ACCESS_KEY` = "SENIN_AWS_SECRET_ACCESS_KEY"
        *   `AWS_DEFAULT_REGION` = "SENIN_AWS_BOLGEN" (örn: `us-east-1`)

    *   **Yerel Geliştirme - `.streamlit/secrets.toml` Dosyası:**
        Proje kök dizininde `.streamlit` adında bir klasör oluşturun. İçine `secrets.toml` adında bir dosya oluşturun ve aşağıdaki içeriği kendi AWS bilgilerinizle doldurun:
        ```toml
        # .streamlit/secrets.toml
        # ÖNEMLİ: BU DOSYAYI GITHUB'A YÜKLEMEYİN!
        # .gitignore dosyanızda listelendiğinden emin olun.

        AWS_ACCESS_KEY_ID = "SENIN_AWS_ACCESS_KEY_ID_BURAYA"
        AWS_SECRET_ACCESS_KEY = "SENIN_AWS_SECRET_ACCESS_KEY_BURAYA"
        AWS_DEFAULT_REGION = "us-east-1" # Veya tercih ettiğiniz Polly bölgesi
        ```

    *   **Yerel Geliştirme - `.env` Dosyası:**
        Proje kök dizinine bir `.env` dosyası oluşturun ve AWS kimlik bilgilerinizi girin:
        ```env
        # .env
        # ÖNEMLİ: BU DOSYAYI GITHUB'A YÜKLEMEYİN!
        # .gitignore dosyanızda listelendiğinden emin olun.

        AWS_ACCESS_KEY_ID="SENIN_AWS_ACCESS_KEY_ID_BURAYA"
        AWS_SECRET_ACCESS_KEY="SENIN_AWS_SECRET_ACCESS_KEY_BURAYA"
        AWS_DEFAULT_REGION="us-east-1" # Veya tercih ettiğiniz Polly bölgesi
        ```
        `python-dotenv` kütüphanesi kuruluysa `app.py` dosyası bu değişkenleri otomatik olarak yükleyecektir.

    *   **Sistem Ortam Değişkenleri:** Kimlik bilgilerinizi sisteminizin ortam değişkenleri olarak da ayarlayabilirsiniz.

5.  **Streamlit Uygulamasını Çalıştırın:**
    ```bash
    streamlit run app.py
    ```
    Uygulama genellikle tarayıcınızda `http://localhost:8501` adresinde açılacaktır.

## Nasıl Kullanılır?

1.  Uygulama açıldığında, kenar çubuğundan tercih ettiğiniz arayüz dilini (Türkçe/İngilizce) seçin.
2.  Kenar çubuğundaki "TTS Dilini Seçin" açılır menüsünden istediğiniz TTS dilini seçin.
3.  "Ses Seçin" açılır menüsünden belirli bir sesi (standart veya nöral) seçin.
4.  Metin alanına dönüştürmek istediğiniz metni girin veya yapıştırın.
5.  "Sesi Oluştur" düğmesine tıklayın.
6.  Ses oluşturulacak ve otomatik olarak çalınacaktır. Ayrıca bir "MP3 Olarak İndir" düğmesi de görünecektir.

## Amazon Polly Hakkında

Amazon Polly, metni canlı gibi konuşmaya dönüştüren bir servistir. Yeni AWS hesapları için Polly, belirli kullanım limitleri dahilinde 12 ay boyunca AWS Ücretsiz Kullanım Katmanı'na dahildir. Bu limitleri aşarsanız veya 12 aylık süre dolduktan sonra standart [Amazon Polly fiyatlandırması](https://aws.amazon.com/polly/pricing/) geçerli olur. Kullanımınızı AWS Management Console'daki Faturalandırma Panosu üzerinden takip edebilirsiniz.

## Katkıda Bulunma

Katkılarınız, sorun bildirimleriniz ve özellik istekleriniz değerlidir! Katkıda bulunmak isterseniz [sorunlar sayfasına](https://github.com/keremalagoz/YOUR_REPOSITORY_NAME/issues) göz atmaktan çekinmeyin.

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - ayrıntılar için `LICENSE` dosyasına bakın (eğer bir lisans dosyası eklerseniz).

---

Geliştiren: Kerem Alagöz
*   **GitHub:** [github.com/keremalagoz](https://github.com/keremalagoz)
*   **LinkedIn:** [linkedin.com/in/keremalagoz](https://www.linkedin.com/in/keremalagoz)