# MarkAI

This project was developed using "Gemini 2.0 Flash Thinking Expermental"
このプロジェクトは"Gemini 2.0 Flash Thinking Expermental"を利用して開発されました

## Project Name: MarkAI

**Description:**

MarkAI is an automated grading system designed to streamline the process of marking student assessments, particularly in subjects like mathematics.  It leverages the power of AI through the Gemini API to analyze images of problems, determine the correctness of answers, and automatically overlay visual marks (like circles for correct answers and crosses for incorrect ones) onto the images.  The system is built as a user-friendly GUI application, making it accessible to educators with varying levels of technical expertise.

**Key Features:**

- AI-Powered Grading: Utilizes the Gemini API to automatically assess student responses from images.
- Automated Marking: Overlays visual "correct" (〇) and "incorrect" (✕) marks directly onto the assessed images.
- User-Friendly GUI:  Provides a graphical user interface built with `tkinter` for easy operation.
- Image-Based Input: Processes grading from images of student work, suitable for handwritten or printed materials.
- Extensible Design:  While initially focused on arithmetic problems, the architecture is designed to be adaptable for grading various subject matters and question formats.
- MIT License: Released under the permissive MIT License, encouraging open contribution and wide usage.

**Intended Benefits:**

MarkAI aims to significantly reduce the workload of educators by automating the time-consuming task of manual grading. By digitizing and automating the marking process, MarkAI contributes to:

- Increased Efficiency:  Speeds up the grading process, freeing up teachers' time.
- Reduced Teacher Workload:  Alleviates the burden of repetitive manual marking tasks.
- Improved Accuracy: Leverages AI to ensure consistent and objective grading.
- Enhanced Digital Assessment:  Facilitates digital workflows for assessment and feedback.

**Target Audience:**

- Teachers and educators at all levels (primary, secondary, higher education).
- Educational institutions seeking to implement or improve digital assessment methods.
- Anyone involved in the creation and grading of problem-based assessments.

## プロジェクト名: MarkAI (マークエーアイ)

**概要:**

MarkAI は、特に算数などの科目における生徒の評価採点プロセスを効率化するために設計された自動採点システムです。 Gemini API を活用して、問題の画像をAIで解析し、解答の正誤を判定、画像上に自動的に視覚的なマーク（正解の場合は〇、不正解の場合は✕など）を重ねて表示します。  システムは、技術的な専門知識のレベルに関わらず、教育者が容易に利用できるよう、ユーザーフレンドリーなGUIアプリケーションとして構築されています。

**主な機能:**

- AIを活用した採点: Gemini API を利用して、画像から生徒の解答を自動的に評価します。
- 自動マーク付け: 評価された画像に、視覚的な「正解」（〇）および「不正解」（✕）マークを直接重ねて表示します。
- ユーザーフレンドリーなGUI:  `tkinter` で構築されたグラフィカルユーザーインターフェースにより、容易な操作性を実現しています。
- 画像ベースの入力: 手書きや印刷物など、生徒の解答を画像として入力し、採点処理を行います。
- 拡張可能な設計:  初期段階では算数問題を対象としていますが、様々な科目や問題形式の採点に適応できるよう設計されています。
- MITライセンス: 寛容なMITライセンスの下で公開されており、オープンな貢献と広範な利用を奨励しています。

**期待される効果:**

MarkAI は、時間のかかる手動採点作業を自動化することで、教育者の負担を大幅に軽減することを目指しています。 採点プロセスをデジタル化および自動化することにより、MarkAI は以下に貢献します。

- 効率の向上: 採点プロセスを迅速化し、教員の時間を有効活用できるようにします。
- 教員の負担軽減: 反復的な手動採点作業の負担を軽減します。
- 精度の向上: AIを活用して、一貫性と客観性のある採点を実現します。
- デジタル評価の促進: 評価とフィードバックのためのデジタルワークフローを促進します。

**対象ユーザー:**

- 小学校、中学校、高校、高等教育機関の教員および教育関係者。
- デジタル評価手法の導入または改善を検討している教育機関。
- 問題形式の評価の作成および採点に関わる全ての方。

はい、承知いたしました。MarkAIの始め方に関する日本語の文章を、UIのボタン名は日本語のまま、英語に翻訳します。以下に翻訳結果を示します。

## Getting Started

Are you ready to automate your grading process with MarkAI? To get started, please follow the steps below.

### Prerequisites

Before using MarkAI, ensure that your system has the following prerequisites installed:

- **Python 3.x**: MarkAI is built using Python 3, which is required to run it. If you do not have Python installed, you can download it from the official website: [Download Python](https://www.python.org/downloads/)

- **Required Python Libraries**: MarkAI relies on several Python libraries for its functionality. These can be easily installed using `pip`, Python's package installer. Open your terminal or command prompt and run the following command:

  ```bash
  pip install Pillow google-generativeai opencv-python
  ```

  This command will install the necessary libraries:
  - `Pillow`: For image processing.
  - `google-generativeai`: The official client library for interacting with the Gemini API.
  - `opencv-python`: For advanced image processing tasks (although not directly used in `main.py` in this version, it is used in `create_grid_image.py`).

  - **Gemini API Key**: MarkAI utilizes the Gemini API for AI-powered grading. To use this feature, you need to obtain an API key from Google AI Studio and set it as an environment variable named `GEMINI_API_KEY`.

    **How to Obtain a Gemini API Key:**

    1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and sign in with your Google account.
    2. If you haven't created a project yet, create a new project.
    3. Within your project, navigate to the "API keys" section (usually found in settings or configuration).
    4. Generate a new API key.
    5. **Set as Environment Variable**: Once you have obtained your API key, you need to set it as an environment variable named `GEMINI_API_KEY`. The method for setting environment variables varies depending on your operating system.

        * **Windows**:

          ```bash
          setx GEMINI_API_KEY "YOUR_API_KEY"  /m
          ```

          (Note: `/m` sets it system-wide. You may need to restart your command prompt or computer for it to take effect.)

        * **macOS/Linux**:

          ```bash
          export GEMINI_API_KEY="YOUR_API_KEY"
          ```

          (Note: This sets it only for the current terminal session. To make it permanent, you should add this line to your shell configuration file, such as `.bashrc` or `.zshrc`.)

        **Replace `"YOUR_API_KEY"` with your actual Gemini API key.**

### Installation

MarkAI does not require a formal installation process. To prepare the project, follow these steps:

1. **Download or Clone**: Download the MarkAI project files as a ZIP archive or clone the repository from GitHub (once it is made public).
2. **Extract (if ZIP download)**: If you downloaded a ZIP file, extract its contents to any directory on your computer.
3. **Navigate to Project Directory**: Open your terminal or command prompt and change the current directory to where you extracted or cloned the MarkAI project files. You should see files like `main.py`, `add_marks_to_image.py`, etc., in this directory.

### Basic Usage: Grading Images

Let's walk through the basic steps to use MarkAI for grading a set of images.

1. **Launch MarkAI Application**: In your terminal or command prompt, from the MarkAI project directory, run the `main.py` script:

  ```bash
  python main.py
  ```

  This will launch the MarkAI graphical user interface (GUI).

2. **Select Image Folder**: In the MarkAI GUI, click the "**画像フォルダ選択**" button. A file dialog will open. Select the folder containing the student worksheets images you want to grade. These images should be in formats like PNG, JPG, or JPEG.

3. **Load Position Information JSON File**: Next, click the "**位置情報JSON読込**" button. Another file dialog will appear. Select the JSON file you created using `position_config_tool.py`. This JSON file contains the positional information for the answer areas on your specific worksheet template. If you haven't created this file yet, you will need to define the answer positions for your worksheet template first using `position_config_tool.py`.

4. **Start Grading Process**: Once both the image folder and the position information JSON file are selected, click the "**採点開始**" button. MarkAI will begin processing each image in the selected folder.

5. **Monitor Progress**: The "**進捗状況:**" text area in the GUI will display progress messages. You will see messages indicating each image being processed, interactions with the Gemini API, and mark overlay operations.

6. **Check for Errors**: If any errors occur during the process, error messages will be displayed in the "**エラーメッセージ:**" text area, and a pop-up error message box may appear. Review these messages to understand and troubleshoot any issues.

7. **Review Graded Images**: Once the grading process is complete (indicated by the message "採点処理が完了しました。"), the marked images (images with overlaid 〇 and ✕ marks) will be saved in a newly created folder named `marked_images` within the MarkAI project directory. The original images will remain unchanged.

### Creating Position Information JSON File (Using `position_config_tool.py`)

To use MarkAI effectively, you first need to create a position information JSON file for your specific worksheet template. This file tells MarkAI the locations of the answer areas within the worksheet image, allowing it to overlay marks correctly.

1. **Prepare Template Image**: Prepare a sample image of your worksheet template (e.g., a blank worksheet or a sample question sheet).

2. **Run `position_config_tool.py`**: Execute the `position_config_tool.py` script:

  ```bash
  python position_config_tool.py
  ```

  This will launch the position configuration tool GUI.

3. **Load Template Image**: In the position configuration tool GUI, click "**画像を開く**" and select your worksheet template image.

4. **Define Problem Positions**: For each problem on the worksheet template:

    - Enter the "問題番号" (Problem Number) in the input field (e.g., 1, 2, 3...).
    - Drag and draw a rectangle over the area where you want to place the mark (〇 or ✕) for that problem.
    - Click "**位置情報を登録**" (Register Position Information) to save the position for that problem.
    - Repeat for all problems on the worksheet.

5. **Save Position Information JSON**: Once you have defined positions for all problems, click "**JSON保存**" (Save JSON) and choose where to save the position information JSON file and what to name it (e.g., `problem_positions.json`). Remember this filename and location, as you will need to load it in `main.py` during the grading process.

## 始め方

MarkAI で採点プロセスを自動化する準備はできましたか？  始めるには、以下の手順に従ってください。

### 前提条件

MarkAI を使用する前に、システムに以下の前提条件がインストールされていることを確認してください。

- **Python 3.x**: MarkAI は Python 3 を使用して構築されており、実行には Python 3 が必要です。 Python がインストールされていない場合は、公式ウェブサイトからダウンロードできます。[Python をダウンロード](https://www.python.org/downloads/)

- **必須 Python ライブラリ**: MarkAI は、その機能のためにいくつかの Python ライブラリに依存しています。これらは Python のパッケージインストーラーである `pip` を使用して簡単にインストールできます。ターミナルまたはコマンドプロンプトを開き、次のコマンドを実行してください。

  ```bash
  pip install Pillow google-generativeai opencv-python
  ```

  このコマンドは、必要なライブラリをインストールします。
  - `Pillow`: 画像処理用。
  - `google-generativeai`: Gemini API と対話するための公式クライアントライブラリ。
  - `opencv-python`: 高度な画像処理タスク用 (このバージョンでは `main.py` で直接使用されていませんが、`create_grid_image.py` で使用されています)。

  - **Gemini API キー**: MarkAI は AI を活用した採点のために Gemini API を利用します。この機能を使用するには、Google AI Studio から API キーを取得し、`GEMINI_API_KEY` という名前の環境変数として設定する必要があります。

    **Gemini API キーの取得方法:**

    1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセスし、Google アカウントでサインインします。

    2. まだプロジェクトを作成していない場合は、新しいプロジェクトを作成します。

    3. プロジェクト内で、「API キー」セクション（通常は設定または構成にあります）に移動します。

    4. 新しい API キーを生成します。

    5. **環境変数として設定**: API キーを取得したら、`GEMINI_API_KEY` という名前の環境変数として設定する必要があります。環境変数を設定する方法は、オペレーティングシステムによって異なります。

          * **Windows**:

            ```bash
            setx GEMINI_API_KEY "YOUR_API_KEY"  /m
            ```

            (注意: `/m` はシステム全体に設定します。反映させるには、コマンドプロンプトまたはコンピュータの再起動が必要になる場合があります。)

          * **macOS/Linux**:

            ```bash
            export GEMINI_API_KEY="YOUR_API_KEY"
            ```

            (注意: これは現在のターミナルセッションのみに設定されます。永続的にするには、この行をシェル構成ファイル (`.bashrc` や `.zshrc` など) に追加する必要があります。)

        **`"YOUR_API_KEY"` を実際の Gemini API キーに置き換えてください。**

### インストール

MarkAI は正式なインストールプロセスを必要としません。プロジェクトを準備するには、次の手順に従ってください。

1. **ダウンロードまたはクローン**: MarkAI プロジェクトファイルを ZIP アーカイブとしてダウンロードするか、GitHub からリポジトリをクローンします (公開後)。
2. **展開 (ZIP ダウンロードの場合)**: ZIP ファイルをダウンロードした場合は、コンピュータ上の任意のディレクトリに内容を解凍します。
3. **プロジェクトディレクトリに移動**: ターミナルまたはコマンドプロンプトを開き、現在のディレクトリを MarkAI プロジェクトファイルを解凍またはクローンした場所に変更します。このディレクトリに `main.py`、`add_marks_to_image.py` などのファイルがあるはずです。

### 基本的な使い方: 画像の採点

MarkAI を使用して画像セットを採点する基本的な手順を見ていきましょう。

1. **MarkAI アプリケーションを起動**: ターミナルまたはコマンドプロンプトで、MarkAI プロジェクトディレクトリから `main.py` スクリプトを実行します。

    ```bash
    python main.py
    ```

    これにより、MarkAI グラフィカルユーザーインターフェース (GUI) が起動します。

2. **画像フォルダを選択**: MarkAI GUI で、"**画像フォルダ選択**" ボタンをクリックします。ファイルダイアログが開きます。採点したい生徒のワークシート画像の入ったフォルダを選択します。これらの画像は、PNG、JPG、JPEG などの形式である必要があります。

3. **位置情報 JSON ファイルを読み込む**: 次に、"**位置情報JSON読込**" ボタンをクリックします。別のファイルダイアログが表示されます。`position_config_tool.py` を使用して作成した JSON ファイルを選択します。この JSON ファイルには、特定のワークシートテンプレートの解答領域の位置情報が含まれています。まだこのファイルを作成していない場合は、まず `position_config_tool.py` を使用してワークシートテンプレートの解答位置を定義する必要があります。

4. **採点プロセスを開始**: 画像フォルダと位置情報 JSON ファイルの両方を選択したら、"**採点開始**" ボタンをクリックします。MarkAI は、選択したフォルダ内の各画像の処理を開始します。

5. **進捗状況を監視**: GUI の "**進捗状況:**" テキストエリアに進捗状況を示すメッセージが表示されます。処理中の各画像、Gemini API とのやり取り、マークオーバーレイ操作などのメッセージが表示されます。

6. **エラーの確認**: プロセス中にエラーが発生した場合、"**エラーメッセージ:**" テキストエリアにエラーメッセージが表示され、ポップアップエラーメッセージボックスが表示される場合があります。これらのメッセージを確認して、問題を理解し、トラブルシューティングを行ってください。

7. **採点済み画像を確認**: 採点処理が完了すると ("採点処理が完了しました。" というメッセージで示されます)、マークされた画像 (〇と✕マークが重ねて表示された画像) は、MarkAI プロジェクトディレクトリ内に新しく作成された `marked_images` という名前のフォルダに保存されます。元の画像は変更されません。

### 位置情報 JSON ファイルの作成 (`position_config_tool.py` を使用)

MarkAI を効果的に使用するには、まず特定のワークシートテンプレートの位置情報 JSON ファイルを作成する必要があります。このファイルは、ワークシート画像内の解答領域の位置を MarkAI に指示し、マークを正しく重ねて表示できるようにします。

1. **テンプレート画像を準備**: ワークシートテンプレートのサンプル画像 (空白のワークシートまたはサンプル問題シートなど) を用意します。

2. **`position_config_tool.py` を実行**: `position_config_tool.py` スクリプトを実行します。

    ```bash
    python position_config_tool.py
    ```

    これにより、位置情報設定ツール GUI が起動します。

3. **テンプレート画像を読み込む**: 位置情報設定ツール GUI で、"画像を開く" をクリックし、ワークシートテンプレート画像を選択します。

4. **問題位置を定義**: ワークシートテンプレート上の各問題について:

      - "問題番号" を入力フィールドに入力します (例: 1、2、3...)。
      - その問題のマーク (〇または✕) を配置する領域上に、長方形をドラッグして描画します。
      - "位置情報を登録" をクリックして、その問題の位置を保存します。
      - ワークシート上のすべての問題について繰り返します。

5. **位置情報 JSON を保存**: すべての問題の位置を定義したら、"JSON保存" をクリックし、位置情報 JSON ファイルを保存する場所とファイル名 (例: `problem_positions.json`) を選択します。このファイル名と場所は、採点時に `main.py` で読み込む必要があるため、覚えておいてください。
