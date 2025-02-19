import tkinter as tk
from tkinter import filedialog, messagebox, Label, Entry, Button, Canvas, Scrollbar, BOTH, VERTICAL, HORIZONTAL
from PIL import Image, ImageTk, UnidentifiedImageError
import json

class PositionConfigTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("位置情報設定ツール")
        self.geometry("1000x800") # ウィンドウサイズを少し大きく

        self.image_path = ""
        self.grid_image_tk = None
        self.positions = {"問題位置情報": []} # 位置情報を格納する辞書

        # --- GUI要素の作成 ---
        # 1. 画像表示エリア
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=BOTH, expand=True) # 左右に配置、余白、伸縮

        self.canvas_scrollbar_y = Scrollbar(self.canvas_frame, orient=VERTICAL)
        self.canvas_scrollbar_x = Scrollbar(self.canvas_frame, orient=HORIZONTAL)

        self.canvas = Canvas(self.canvas_frame, bd=0, xscrollcommand=self.canvas_scrollbar_x.set, yscrollcommand=self.canvas_scrollbar_y.set, relief=tk.SUNKEN) # Scrollbarと連携、凹んだ枠線

        self.canvas_scrollbar_y.config(command=self.canvas.yview)
        self.canvas_scrollbar_x.config(command=self.canvas.xview)

        self.canvas_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.TOP, fill=BOTH, expand=True) # Frame内で伸縮

        self.canvas.bind("<Button-1>", self.on_canvas_click) # クリックイベント

        # 2. 設定エリア (右側)
        self.config_frame = tk.Frame(self)
        self.config_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y) # 右側に配置、余白、上下に伸縮

        # 2-1. ファイル操作ボタン
        self.file_frame = tk.Frame(self.config_frame)
        self.file_frame.pack(fill=tk.X, pady=5)

        Button(self.file_frame, text="画像を開く", command=self.load_image).pack(side=tk.LEFT, padx=5)
        Button(self.file_frame, text="JSON保存", command=self.save_json).pack(side=tk.LEFT, padx=5)
        Button(self.file_frame, text="JSON読込", command=self.load_json).pack(side=tk.LEFT, padx=5)

        # 2-2. 問題番号設定
        self.problem_frame = tk.Frame(self.config_frame)
        self.problem_frame.pack(fill=tk.X, pady=5)
        Label(self.problem_frame, text="問題番号:").pack(side=tk.LEFT)
        self.problem_number_entry = Entry(self.problem_frame, width=5)
        self.problem_number_entry.pack(side=tk.LEFT)

        # 2-3. 位置情報表示 (X, Y座標)
        self.position_frame = tk.Frame(self.config_frame)
        self.position_frame.pack(fill=tk.X, pady=5)
        Label(self.position_frame, text="X座標:").pack(side=tk.LEFT)
        self.x_pos_label = Label(self.position_frame, text="-")
        self.x_pos_label.pack(side=tk.LEFT)
        Label(self.position_frame, text="Y座標:").pack(side=tk.LEFT)
        self.y_pos_label = Label(self.position_frame, text="-")
        self.y_pos_label.pack(side=tk.LEFT)

        # 2-4. 位置情報登録ボタン
        Button(self.config_frame, text="位置情報を登録", command=self.register_position).pack(pady=10)

        # 2-5. 問題リスト表示 (Treeviewにするとより高機能だが、今回はLabelで簡易的に)
        self.problem_list_frame = tk.Frame(self.config_frame, bd=1, relief=tk.SUNKEN) # 枠線
        self.problem_list_frame.pack(fill=tk.BOTH, expand=True, pady=10) # 伸縮、縦方向にも広げる
        Label(self.problem_list_frame, text="登録済み問題リスト", bd=0).pack(fill=tk.X) # タイトル
        self.problem_list_label = Label(self.problem_list_frame, text="", justify=tk.LEFT, anchor=tk.NW) # 左寄せ、上寄せ
        self.problem_list_label.pack(fill=tk.BOTH, expand=True) # 伸縮

    def load_image(self):
        """画像ファイルを開く処理"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if not file_path:
            return

        try:
            self.image_path = file_path
            pil_image = Image.open(file_path)
            self.grid_image_tk = ImageTk.PhotoImage(pil_image) # PhotoImageに変換

            self.canvas.config(scrollregion=(0, 0, pil_image.width, pil_image.height)) # Scroll領域設定
            self.canvas.create_image(0, 0, image=self.grid_image_tk, anchor="nw") # 画像をCanvasに配置

            messagebox.showinfo("画像読み込み", "画像を読み込みました")
            self.update_problem_list_display() # 画像読み込み時にリスト更新

        except FileNotFoundError:
            messagebox.showerror("ファイルエラー", "画像ファイルが見つかりません")
        except UnidentifiedImageError:
            messagebox.showerror("ファイルエラー", "画像ファイル形式が不正です")
        except Exception as e:
            messagebox.showerror("エラー", f"予期せぬエラーが発生しました: {e}")


    def save_json(self):
        """JSONファイルを保存する処理"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.positions, f, indent=4, ensure_ascii=False) # JSONを書き込み、インデントと日本語対応
            messagebox.showinfo("JSON保存", "位置情報をJSONファイルに保存しました")
        except Exception as e:
            messagebox.showerror("エラー", f"JSONファイル保存中にエラーが発生しました: {e}")


    def load_json(self):
        """JSONファイルを読み込む処理"""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.positions = json.load(f) # JSONを読み込み
            messagebox.showinfo("JSON読込", "位置情報をJSONファイルから読み込みました")
            self.update_problem_list_display() # JSON読み込み時にリスト更新
        except Exception as e:
            messagebox.showerror("エラー", f"JSONファイル読み込み中にエラーが発生しました: {e}")


    def on_canvas_click(self, event):
        """Canvasクリック時のイベント処理"""
        x = self.canvas.canvasx(event.x) # Canvas座標に変換
        y = self.canvas.canvasy(event.y)
        self.x_pos_label.config(text=str(int(x))) # 整数で表示
        self.y_pos_label.config(text=str(int(y)))


    def register_position(self):
        """位置情報を登録する処理"""
        problem_number_str = self.problem_number_entry.get()
        x_pos_str = self.x_pos_label.cget("text") # Labelからテキストを取得
        y_pos_str = self.y_pos_label.cget("text")

        if not problem_number_str:
            messagebox.showerror("入力エラー", "問題番号を入力してください")
            return
        if x_pos_str == "-" or y_pos_str == "-":
            messagebox.showerror("入力エラー", "Canvasをクリックして位置を指定してください")
            return

        try:
            problem_number = int(problem_number_str)
            x_pos = int(x_pos_str)
            y_pos = int(y_pos_str)
        except ValueError:
            messagebox.showerror("入力エラー", "問題番号、X座標、Y座標は整数で入力してください")
            return

        # 既存の問題番号かチェック
        for problem_info in self.positions["問題位置情報"]:
            if problem_info["問題番号"] == problem_number:
                problem_info["正解位置"] = {"x": x_pos, "y": y_pos} # 上書き
                messagebox.showinfo("情報更新", f"問題番号 {problem_number} の位置情報を更新しました")
                self.update_problem_list_display() # リスト表示更新
                return # 更新したら処理を終える

        # 新規問題番号の場合、リストに追加
        new_problem_info = {
            "問題番号": problem_number,
            "正解位置": {"x": x_pos, "y": y_pos}
        }
        self.positions["問題位置情報"].append(new_problem_info)
        messagebox.showinfo("情報登録", f"問題番号 {problem_number} の位置情報を登録しました")
        self.update_problem_list_display() # リスト表示更新


    def update_problem_list_display(self):
        """登録済み問題リストをLabelに表示更新"""
        problem_list_text = ""
        if self.image_path:
            problem_list_text += f"画像ファイル: {self.image_path}\n\n" # ファイル名表示

        if self.positions["問題位置情報"]:
            problem_list_text += "--- 登録済み問題 ---\n"
            for problem_info in sorted(self.positions["問題位置情報"], key=lambda x: x["問題番号"]): # 問題番号順にソート
                problem_list_text += f"問題{problem_info['問題番号']}: X={problem_info['正解位置']['x']}, Y={problem_info['正解位置']['y']}\n"
        else:
            problem_list_text += "位置情報はまだ登録されていません\n"

        self.problem_list_label.config(text=problem_list_text) # Labelを更新


if __name__ == "__main__":
    app = PositionConfigTool()
    app.mainloop()