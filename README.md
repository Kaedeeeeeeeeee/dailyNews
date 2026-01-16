# AI News Collector

每日自動で X/Twitter から AI 関連ニュースを収集し、日本語に翻訳して Markdown ドキュメントを生成します。

## 🚀 機能

- X/Twitter から24時間以内の投稿を自動収集
- Gemini AI を使用して AI 関連コンテンツをフィルタリング
- 300文字以内の要約を自動生成
- 日本語への自動翻訳
- 画像の自動ダウンロードと最適化
- Markdown 形式で出力
- GitHub Actions による毎日の自動実行

## 📋 必要条件

- Python 3.11+
- X/Twitter アカウント
- Gemini API Key

## 🔧 セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

```bash
cp .env.example .env
# .env ファイルを編集して認証情報を入力
```

必要な環境変数:
- `X_USERNAME`: X のユーザー名
- `X_PASSWORD`: X のパスワード
- `GEMINI_API_KEY`: Gemini API Key

### 3. ローカル実行

```bash
python main.py
```

## 📁 プロジェクト構造

```
dailyNews/
├── .github/workflows/    # GitHub Actions
├── config/               # 設定ファイル
├── src/                  # ソースコード
├── templates/            # テンプレート
├── output/               # 出力ディレクトリ
├── logs/                 # ログ
└── tests/                # テスト
```

## 🤖 GitHub Actions

毎日 JST 6:30 に自動実行されます。手動実行も可能です。

## 📝 ライセンス

MIT License
