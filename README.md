# マインスイーパー (Minesweeper)

Pythonで実装されたシンプルなマインスイーパーゲームです。

## 特徴

- 初級、中級、上級の難易度選択
- カスタム難易度設定
- 日本語インターフェース
- シンプルで使いやすいUI

## 必要条件

- Python 3.6以上
- Tkinter（Pythonのグラフィカルユーザーインターフェースライブラリ）

## インストール方法

### 1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/minesweeper.git
cd minesweeper
```

### 2. Tkinterのインストール

#### Ubuntuの場合:
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

#### macOSの場合:
通常はPythonに同梱されていますが、必要に応じて:
```bash
brew install python-tk
```

#### Windowsの場合:
通常はPythonインストーラーに含まれています。

## 実行方法

```bash
python minesweeper.py
```

## 遊び方

1. 難易度を選択します（初級、中級、上級、またはカスタム）
2. 左クリックでセルを開きます
3. 右クリックで地雷の可能性があるセルに旗を立てます
4. すべての地雷以外のセルを開くとゲームクリアです
5. 地雷を踏むとゲームオーバーです

## スクリーンショット

（スクリーンショットを追加予定）

## ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
