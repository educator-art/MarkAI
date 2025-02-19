from PIL import Image, ImageDraw, ImageFont
import json

def add_marks_from_json(image_path, json_path, results, correct_mark_path="circle_red.png", incorrect_mark_path="cross_red.png"):
    """
    JSONファイルに定義された位置情報に基づいて、
    正誤結果（results）に応じて画像に〇または✕マークを合成する関数

    Args:
        image_path: 	元の計算問題画像のファイルパス
        json_path: 	 位置情報が記述されたJSONファイルのファイルパス
        results: 		問題番号と正誤結果の辞書 (例: {1: True, 2: False, 3: True, ...})
                        True: 正解, False: 不正解
        correct_mark_path: 正解マーク画像 (〇) のファイルパス (PNG推奨)
        incorrect_mark_path: 不正解マーク画像 (✕) のファイルパス (PNG推奨)
    Returns:
        Image: マークが合成されたPIL Imageオブジェクト (合成失敗時は None)
    """
    try:
        # 1. JSONファイルの読み込み
        with open(json_path, 'r', encoding='utf-8') as f:
            position_data = json.load(f)

        # 2. 画像とマーク画像の読み込み
        base_image = Image.open(image_path).convert("RGBA") # 元画像をRGBAで読み込み (透明度対応)
        mark_image_correct = Image.open(correct_mark_path).convert("RGBA") # 〇画像
        mark_image_incorrect = Image.open(incorrect_mark_path).convert("RGBA") # ✕画像

        # デバッグ用: 画像のモードとサイズを確認
        print(f"base_image mode: {base_image.mode}, size: {base_image.size}")
        print(f"mark_image_correct mode: {mark_image_correct.mode}, size: {mark_image_correct.size}")
        print(f"mark_image_incorrect mode: {mark_image_incorrect.mode}, size: {mark_image_incorrect.size}")

        # 3. 合成用透明RGBA画像を作成し、元画像をペースト
        合成画像 = Image.new("RGBA", base_image.size, (0, 0, 0, 0)) # 透明RGBA画像
        合成画像 = Image.alpha_composite(合成画像, base_image) # 元画像を合成

        # 4. JSONの位置情報に基づいて、〇または✕を合成
        for problem_info in position_data["問題位置情報"]:
            problem_number = problem_info["問題番号"]
            correct_position = problem_info["正解位置"] # 正解位置のみ使用 (〇と✕で同じ位置)

            # 問題番号を文字列に変換してから results を参照するように修正
            problem_number_str = str(problem_number)
            if problem_number_str in results:
                is_correct = results[problem_number_str] # 正誤結果を取得
                mark_to_use = mark_image_correct if is_correct else mark_image_incorrect # 使用するマーク画像を選択
                position = (correct_position["x"] - mark_to_use.width // 2,
                            correct_position["y"] - mark_to_use.height // 2) # 中心を位置合わせ

                合成画像.paste(mark_to_use, position, mask=mark_to_use) # アルファマスク合成 (paste のみを使用)


        return 合成画像 # 合成後のPIL Imageオブジェクトを返す

    except FileNotFoundError as e:
        print(f"ファイルが見つかりません: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSONファイル形式エラー: {e}")
        return None
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return None


# --- 実行例 ---
if __name__ == "__main__":
    image_file = "keisan_problem.png" # 元の計算問題画像 (グリッド線なし)
    json_file = "problem_positions.json" # 位置情報JSONファイル (GUIツールで作成)
    output_file = "marked_image.png" # マーク合成後の出力ファイル名
    correct_mark_file = "circle_red.png" # 赤丸画像ファイル
    incorrect_mark_file = "cross_red.png" # 赤バツ画像ファイル

    # --- 	正誤結果の例 (実際には、自動採点ロジックや外部からの入力で決定) 	---
    problem_results = {
        "1": True, 	# 1番の問題は正解 (キーを文字列に修正)
        "2": False, # 2番の問題は不正解 (キーを文字列に修正)
        "3": True, 	# 3番の問題は正解 (キーを文字列に修正)
        #4: True,
        #5: False,
        # ... 必要に応じて増やす
    }

    marked_image = add_marks_from_json(image_file, json_file, problem_results, correct_mark_file, incorrect_mark_file)

    if marked_image:
        output_file_path = f"marked_image_{image_file}" # 出力ファイル名に元画像ファイル名を含める
        marked_image.save(output_file_path) # 画像を保存
        print(f"マークを合成した画像を {output_file_path} に保存しました。")
        # marked_image.show() # 画像をプレビュー表示 (必要に応じて)
    else:
        print("画像の合成に失敗しました。")