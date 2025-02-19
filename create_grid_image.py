import cv2
import numpy as np

def draw_grid(image_path, output_path, grid_interval_x=50, grid_interval_y=50, grid_color=(192, 192, 192), grid_thickness=1):
    """
    画像にグリッド線を描画する関数

    Args:
        image_path:     元の画像のファイルパス
        output_path:    グリッド線を描画した画像の出力ファイルパス
        grid_interval_x: X軸方向のグリッド間隔 (ピクセル)
        grid_interval_y: Y軸方向のグリッド間隔 (ピクセル)
        grid_color:      グリッド線の色 (BGR形式, 例: グレー=(192, 192, 192))
        grid_thickness:  グリッド線の太さ (ピクセル)
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"画像ファイルが見つかりません: {image_path}")

        height, width = img.shape[:2]

        # 縦方向のグリッド線
        for x in range(grid_interval_x, width, grid_interval_x):
            cv2.line(img, (x, 0), (x, height), grid_color, grid_thickness)

        # 横方向のグリッド線
        for y in range(grid_interval_y, height, grid_interval_y):
            cv2.line(img, (0, y), (width, y), grid_color, grid_thickness)

        cv2.imwrite(output_path, img)
        print(f"グリッド線付き画像を {output_path} に保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")


# --- 実行例 ---
if __name__ == "__main__":
    original_image_file = "keisan_problem.png" # 元の計算問題画像 (例として用意)
    grid_image_file = "keisan_problem_grid.png" # グリッド線付き画像の出力ファイル名

    draw_grid(original_image_file, grid_image_file) # グリッド線描画を実行
    # 必要に応じて、グリッド間隔や色などを調整して再度実行してください