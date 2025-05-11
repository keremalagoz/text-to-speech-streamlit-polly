# Text-to-Speech (TTS) with Amazon Polly - Streamlit App

This is an interactive web application built with [Streamlit](https://streamlit.io/) and Amazon Web Services (AWS) [Polly](https://aws.amazon.com/polly/) that converts text into natural-sounding speech.

🌐 **[View Live Demo (if deployed)](YOUR_STREAMLIT_APP_URL_HERE)**  _(Replace with your actual app URL)_

🇹🇷 **[Türkçe Açıklama (Turkish Description)](README_tr.md)**

## Features

*   Convert user-input text to speech.
*   Select from a wide range of Amazon Polly voices across multiple languages and regions.
*   Choose between standard and neural (NTTS) voices for higher quality.
*   Listen to the generated audio directly in the browser.
*   Download the generated audio as an MP3 file.
*   User interface available in English and Turkish.
*   Responsive design, usable on mobile and desktop devices.

## Screenshots

_(Add a screenshot of your application here. You can drag and drop an image into the GitHub editor or use Markdown's image syntax: ![App Screenshot](path/to/your/screenshot.png))_

## Setup and Running

### Prerequisites

*   Python 3.8 or higher.
*   An AWS Account.
*   An IAM user with programmatic access and permissions to use the Amazon Polly service (e.g., `AmazonPollyReadOnlyAccess` or `AmazonPollyFullAccess` if you plan to use features like lexicons). You will need the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` for this user.
*   Your preferred AWS Region where Polly is available (e.g., `us-east-1`, `eu-west-1`). This will be your `AWS_DEFAULT_REGION`.

### Steps

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
        If you deploy the app to Streamlit Community Cloud, add your credentials as "Secrets" in your app's settings:
        *   `AWS_ACCESS_KEY_ID` = "YOUR_AWS_ACCESS_KEY_ID"
        *   `AWS_SECRET_ACCESS_KEY` = "YOUR_AWS_SECRET_ACCESS_KEY"
        *   `AWS_DEFAULT_REGION` = "YOUR_AWS_REGION" (e.g., `us-east-1`)

    *   **For Local Development - `.streamlit/secrets.toml` File:**
        Create a folder named `.streamlit` in the project root. Inside it, create a file named `secrets.toml` with the following content:
        ```toml
        # .streamlit/secrets.toml
        # IMPORTANT: DO NOT COMMIT THIS FILE TO GITHUB!
        # Ensure it's listed in your .gitignore file.

        AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY_ID_HERE"
        AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY_HERE"
        AWS_DEFAULT_REGION = "us-east-1" # Or your preferred Polly region
        ```

    *   **For Local Development - `.env` File:**
        Create a `.env` file in the project root and add your AWS credentials:
        ```env
        # .env
        # IMPORTANT: DO NOT COMMIT THIS FILE TO GITHUB!
        # Ensure it's listed in your .gitignore file.

        AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID_HERE"
        AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY_HERE"
        AWS_DEFAULT_REGION="us-east-1" # Or your preferred Polly region
        ```
        The `app.py` file will automatically load these variables if `python-dotenv` is installed.

    *   **System Environment Variables:** You can also set your credentials as system environment variables.

5.  **Run the Streamlit Application:**
    ```bash
    streamlit run app.py
    ```
    The application will typically open in your browser at `http://localhost:8501`.

## How to Use

1.  When the application opens, select your preferred UI language (English/Turkish) from the sidebar.
2.  Choose the desired TTS language from the "Select TTS Language" dropdown in the sidebar.
3.  Select a specific voice (standard or neural) from the "Select Voice" dropdown.
4.  Enter or paste the text you want to convert into the text area.
5.  Click the "Generate Audio" button.
6.  The audio will be generated and played automatically. A "Download as MP3" button will also appear.

## About Amazon Polly

Amazon Polly is a service that turns text into lifelike speech. For new AWS accounts, Polly is included in the AWS Free Tier for 12 months, with certain usage limits. If you exceed these limits or after the 12-month period, standard [Amazon Polly pricing](https://aws.amazon.com/polly/pricing/) will apply. You can monitor your usage through the AWS Management Console's Billing Dashboard.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/keremalagoz/YOUR_REPOSITORY_NAME/issues) if you want to contribute.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details (if you add a license file).

---

Developed by Kerem Alagöz
*   **GitHub:** [github.com/keremalagoz](https://github.com/keremalagoz)
*   **LinkedIn:** [linkedin.com/in/keremalagoz](https://www.linkedin.com/in/keremalagoz)