import tkinter as tk
from tkinter import filedialog, messagebox, Text, Scrollbar, BOTH, VERTICAL, Y, Menu
import os
from PIL import Image, ImageTk, ImageDraw  # ImageDraw をインポート

# --- 4つの機能をモジュールとしてインポート ---
import create_grid_image
import position_config_tool # position_config_tool.py はGUIツールなので、ここでは直接機能は使用しないが、インポートしておく
import add_marks_to_image
import get_gemini_results_json

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("自動採点システム GUI")
        self.geometry("1000x800") # ウィンドウサイズを少し大きく

        # --- クラス変数 ---
        self.image_folder_path = "" # 画像フォルダパス
        self.position_json_path = "" # 位置情報JSONファイルパス
        self.output_folder_path = "marked_images" # デフォルト出力フォルダ
        self.progress_text = None # 進捗状況表示エリア (Textウィジェット)
        self.error_text = None # エラーメッセージ表示エリア (Textウィジェット)

        # --- マーク画像ファイルのパス (デフォルト) ---
        self.correct_mark_path = "circle_red.png" # 〇マーク (赤)
        self.incorrect_mark_path = "cross_red.png" # ✕マーク (赤)

        self.create_widgets() # GUI 部品を作成・配置

    def create_widgets(self):
        """GUI 部品を作成・配置"""

        # --- メニューバー ---
        self.create_menu_bar()

        # --- フレームの作成 ---
        input_frame = tk.Frame(self) # 入力ファイル選択用フレーム
        input_frame.pack(pady=10)

        output_frame = tk.Frame(self) # 出力設定用フレーム
        output_frame.pack(pady=5)

        process_frame = tk.Frame(self) # 処理実行用フレーム
        process_frame.pack(pady=10)

        status_frame = tk.Frame(self) # 進捗・エラー表示フレーム
        status_frame.pack(pady=10, fill=BOTH, expand=True)

        # --- 入力ファイル選択 ---
        # 1. 画像フォルダ選択
        tk.Button(input_frame, text="画像フォルダ選択", command=self.select_image_folder).pack(side=tk.LEFT, padx=5)
        # 2. 位置情報JSONファイル読込
        tk.Button(input_frame, text="位置情報JSON読込", command=self.load_position_json).pack(side=tk.LEFT, padx=5)

        # --- 出力設定 ---
        # 3. 出力フォルダ設定 (必要に応じて)
        # Label(output_frame, text="出力フォルダ:").pack(side=tk.LEFT, padx=5) # 必要であれば出力フォルダ設定を追加
        # tk.Entry(output_frame, width=40).pack(side=tk.LEFT, padx=5) # 必要であれば出力フォルダ設定を追加

        # --- 処理実行ボタン ---
        # 4. 採点開始ボタン
        tk.Button(process_frame, text="採点開始", font=("Helvetica", 12, "bold"), command=self.start_grading).pack(side=tk.LEFT, padx=10)

        # --- 進捗状況表示エリア ---
        tk.Label(status_frame, text="進捗状況:").pack(anchor=tk.NW) # 左上に配置
        self.progress_text = Text(status_frame, height=10, wrap=tk.WORD) #  wrap=tk.WORD: 単語単位で改行
        progress_scrollbar = Scrollbar(status_frame, orient=VERTICAL, command=self.progress_text.yview)
        self.progress_text.config(yscrollcommand=progress_scrollbar.set, state=tk.DISABLED) # 初期状態は編集不可
        progress_scrollbar.pack(side=tk.RIGHT, fill=Y)
        self.progress_text.pack(side=tk.LEFT, fill=BOTH, expand=True)

        # --- エラーメッセージ表示エリア ---
        tk.Label(status_frame, text="エラーメッセージ:").pack(anchor=tk.NW) # 左上に配置, 進捗状況の下に配置したい場合は row=1 などで指定
        self.error_text = Text(status_frame, height=5, wrap=tk.WORD)
        error_scrollbar = Scrollbar(status_frame, orient=VERTICAL, command=self.error_text.yview)
        self.error_text.config(yscrollcommand=error_scrollbar.set, state=tk.DISABLED) # 初期状態は編集不可
        error_scrollbar.pack(side=tk.RIGHT, fill=Y)
        self.error_text.pack(side=tk.LEFT, fill=BOTH, expand=True)


    def create_menu_bar(self):
        """メニューバーを作成"""
        menubar = Menu(self)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="設定", command=self.open_settings_dialog) # 設定画面 (未実装)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.quit)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        self.config(menu=menubar)


    def select_image_folder(self):
        """画像フォルダを選択"""
        self.image_folder_path = filedialog.askdirectory()
        if self.image_folder_path:
            self.progress_log(f"画像フォルダを選択しました: {self.image_folder_path}")


    def load_position_json(self):
        """位置情報JSONファイルを読み込む"""
        self.position_json_path = filedialog.askopenfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if self.position_json_path:
            self.progress_log(f"位置情報JSONファイルを読み込みました: {self.position_json_path}")


    def start_grading(self):
        """採点処理を開始 (コアロジック)"""
        if not self.image_folder_path:
            messagebox.showerror("エラー", "画像フォルダを選択してください")
            return
        if not self.position_json_path:
            messagebox.showerror("エラー", "位置情報JSONファイルを読み込んでください")
            return

        image_files = [f for f in os.listdir(self.image_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not image_files:
            messagebox.showerror("エラー", "画像フォルダに画像ファイルが見つかりません")
            return

        self.progress_log("採点処理を開始します...")
        self.error_clear() # エラー表示エリアをクリア

        os.makedirs(self.output_folder_path, exist_ok=True) # 出力フォルダを作成 (存在していてもOK)

        for image_file in image_files:
            image_path = os.path.join(self.image_folder_path, image_file)
            output_image_path = os.path.join(self.output_folder_path, f"marked_{image_file}") # 出力ファイルパス

            self.progress_log(f"{image_file} の採点処理を開始...")

            try:
                # --- 1. Gemini API連携で正誤結果を取得 ---
                self.progress_log("  Gemini API 連携...")
                problem_results = get_gemini_results_json.get_problem_results_from_gemini_json(image_path)
                if problem_results is None:
                    error_message = f"  Gemini API エラーまたは正誤結果取得失敗: {image_file}"
                    self.error_log(error_message) # エラーメッセージをエラー表示エリアへ
                    continue # 次の画像へ

                # --- 2. 〇×マーク合成 ---
                self.progress_log("  〇×マーク合成...")
                marked_image = add_marks_to_image.add_marks_from_json(
                    image_path,
                    self.position_json_path,
                    problem_results,
                    correct_mark_path=self.correct_mark_path, # マーク画像ファイルパスを渡す
                    incorrect_mark_path=self.incorrect_mark_path # マーク画像ファイルパスを渡す
                )
                if marked_image is None:
                    error_message = f"  〇×マーク合成失敗: {image_file}"
                    self.error_log(error_message) # エラーメッセージをエラー表示エリアへ
                    continue # 次の画像へ

                # --- 3. 採点済み画像を保存 ---
                marked_image.save(output_image_path)
                self.progress_log(f"{image_file} : 採点完了。{output_image_path} に保存")

            except Exception as e: # 予期せぬエラー
                error_message = f"{image_file} : 予期せぬエラー: {e}"
                self.error_log(error_message) # エラーメッセージをエラー表示エリアへ
                messagebox.showerror("エラー", error_message) # MessageBoxでもエラー表示
                continue # 次の画像へ

        self.progress_log("全ての画像の採点処理が完了しました。")
        messagebox.showinfo("完了", "採点処理が完了しました。") # 完了メッセージ


    def open_settings_dialog(self):
        """設定ダイアログを開く (未実装)"""
        messagebox.showinfo("設定", "設定画面はまだ実装されていません。")


    def progress_log(self, message):
        """進捗状況を Text ウィジェットに追記表示 (改行あり)"""
        self.progress_text.config(state=tk.NORMAL) # 編集可能にする
        self.progress_text.insert(tk.END, message + "\n") # テキスト追記
        self.progress_text.see(tk.END) #  一番下にスクロール
        self.progress_text.config(state=tk.DISABLED) # 編集不可に戻す
        self.update_idletasks() #  GUI を更新 (即時反映)


    def error_log(self, message):
        """エラーメッセージを Text ウィジェットに追記表示 (改行あり)"""
        self.error_text.config(state=tk.NORMAL) # 編集可能にする
        self.error_text.insert(tk.END, message + "\n") # エラーメッセージ追記
        self.error_text.see(tk.END)
        self.error_text.config(state=tk.DISABLED) # 編集不可に戻す
        self.update_idletasks()


    def error_clear(self):
        """エラーメッセージ表示エリアをクリア"""
        self.error_text.config(state=tk.NORMAL) # 編集可能にする
        self.error_text.delete("1.0", tk.END) #  すべて削除
        self.error_text.config(state=tk.DISABLED) # 編集不可に戻す
        self.update_idletasks()


if __name__ == "__main__":
    app = MainApplication()

    # --- マーク画像ファイル (〇×) が存在しない場合は、デフォルトの画像を生成して保存 ---
    if not os.path.exists(app.correct_mark_path):
        # デフォルトの〇画像生成 (赤丸)
        mark_size = 60 # マークのサイズ (pixel)
        mark_image = Image.new("RGBA", (mark_size, mark_size), (0, 0, 0, 0)) # 透明RGBA画像
        draw = ImageDraw.Draw(mark_image)
        draw.ellipse((5, 5, mark_size - 5, mark_size - 5), fill=(255, 0, 0, 255), width=5) # 赤丸
        mark_image.save(app.correct_mark_path) # ファイルに保存
        print(f"〇マーク画像 {app.correct_mark_path} を生成しました。") #  初回起動時などにメッセージを表示

    if not os.path.exists(app.incorrect_mark_path):
        # デフォルトの✕画像生成 (赤バツ)
        mark_size = 60
        mark_image = Image.new("RGBA", (mark_size, mark_size), (0, 0, 0, 0)) # 透明RGBA画像
        draw = ImageDraw.Draw(mark_image)
        draw.line((10, 10, mark_size - 10, mark_size - 10), fill=(255, 0, 0, 255), width=8) # 赤バツ斜め線
        draw.line((10, mark_size - 10, mark_size - 10, 10), fill=(255, 0, 0, 255), width=8) # 赤バツ斜め線 (もう一本)
        mark_image.save(app.incorrect_mark_path) # ファイルに保存
        print(f"✕マーク画像 {app.incorrect_mark_path} を生成しました。") # 初回起動時などにメッセージを表示


    app.mainloop()