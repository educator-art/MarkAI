import google.generativeai as genai
import json
from PIL import Image
import os

# Gemini API の API キーを設定
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_problem_results_from_gemini_json(image_path):
    """
    Gemini API を使って画像内の計算問題を解析し、
    正誤結果を JSON 形式で取得する関数

    Args:
        image_path: 計算問題画像のファイルパス
    Returns:
        dict: 問題番号をキー、正誤結果 (True/False) を値とする辞書
              API リクエスト失敗時などは None を返す
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp') # gemini-2.0-flash-exp モデルを使用

        image = Image.open(image_path) # 画像を PIL Image オブジェクトとして読み込み

        # プロンプト (JSON 形式での回答を指示)
        prompt_text = """
        この画像は計算問題です。各問題の正誤判定を行い、
        問題番号をキー、正誤結果 (正解の場合は true, 不正解の場合は false) を値とする JSON 形式の文字列で出力してください。
        JSON 形式の文字列 *のみ* を出力し、それ以外のテキスト、特にコードブロックなどは絶対に出力しないでください。
        """ # ユーザープロンプト

        response = model.generate_content([prompt_text, image]) # テキストと画像を Gemini API に送信
        response.resolve() # レスポンスを resolve (エラーハンドリングのため)

        if response.text: # 回答テキストが存在する場合
            gemini_response_json_string = response.text # 回答テキスト (JSON 形式と期待)

            try:
                problem_results_json = json.loads(gemini_response_json_string) # JSON 文字列を Python 辞書にパース
                # problem_results = problem_results_json.get("problem_results") # "problem_results" キーの値を取得  <-  削除またはコメントアウト

                # if isinstance(problem_results, dict): # 辞書形式であることを確認 <- 修正
                if isinstance(problem_results_json, dict): # problem_results_json自体が辞書形式であることを確認
                    print("Gemini API response (JSON):") # デバッグ用出力
                    print(json.dumps(problem_results_json, indent=4, ensure_ascii=False)) # JSON を整形して表示
                    # return problem_results # パースした辞書を返す <- 修正
                    return problem_results_json # パースした辞書 (problem_results_json) を返す
                else:
                    print("API response format error: 'problem_results' key not found or not a dictionary.") # エラーメッセージ
                    print("Response text:", gemini_response_json_string) # レスポンス全体を表示 (デバッグ用)
                    return None # エラー時は None を返す

            except json.JSONDecodeError as e: # JSON パースエラー
                print(f"JSON Decode Error: {e}") # JSON パースエラーメッセージ
                print("Response text:", gemini_response_json_string) # レスポンス全体を表示 (デバッグ用)
                return None # エラー時は None を返す

        else: # 回答テキストが空の場合 (API エラーの可能性)
            print("Gemini API response text is empty.") # エラーメッセージ
            print("Raw response:", response) # レスポンス全体を表示 (デバッグ用)
            return None # エラー時は None を返す

    except Exception as e: # 予期せぬエラー
        print(f"Gemini API request error: {e}") # エラーメッセージ
        return None # エラー時は None を返す
    

# --- 実行例 ---
if __name__ == "__main__":
    image_file = "keisan_problem.png" # 計算問題画像ファイル

    problem_results = get_problem_results_from_gemini_json(image_file) # Gemini API で正誤結果を取得

    if problem_results: # 辞書形式で正誤結果が取得できた場合
        print("\n--- 取得した正誤結果 ---") # 結果表示
        print(problem_results)

        # ここに、取得した problem_results を add_marks_from_json() に渡して
        # 〇×マーク合成処理を行うコードを追加
        # 例:
        # from add_marks_to_image import add_marks_from_json # (同じフォルダに add_marks_to_image.py がある場合)
        # marked_image = add_marks_to_json(image_file, "problem_positions.json", problem_results)
        # if marked_image:
        #     marked_image.save("marked_image_gemini.png")
        #     print("〇×マーク合成画像を marked_image_gemini.png に保存しました。")
        # else:
        #     print("〇×マーク合成に失敗しました。")

    else: # Gemini API から正誤結果を取得できなかった場合
        print("\nGemini API からの正誤結果取得に失敗しました。") # エラーメッセージ