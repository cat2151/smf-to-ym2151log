# smf-to-ym2151log

**Standard MIDIファイル (SMF) をYM2151レジスタ書き込みログ（JSON形式）に変換**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## 概要

Standard MIDIファイル (SMF) をYM2151レジスタ書き込みログ（JSON形式）に変換します。

## 特徴

- **2パス処理**:
  - **パスA**: MIDIファイルを中間イベントJSON（デバッグ用）に変換
  - **パスB**: イベントをYM2151レジスタ書き込みログJSON（最終出力）に変換
- **テスト駆動開発**: 包括的なユニットテスト
- **モジュラー設計**: 各ソースファイルは約100行に抑えられています
- **互換性のあるフォーマット**: [ym2151-zig-cc](https://github.com/cat2151/ym2151-zig-cc) と互換性のあるJSON形式を出力

## インストール

```bash
pip install -r requirements.txt
```

## 使い方

```bash
python smf_to_ym2151log.py <midi_file>
```

### 例

```bash
# テストMIDIファイルを作成
python create_test_midi.py

# YM2151ログに変換
python smf_to_ym2151log.py test.mid
```

これにより以下のファイルが生成されます:
- `test_events.json` - パスA出力（デバッグイベント）
- `test_ym2151.json` - パスB出力（YM2151ログ）

## 出力フォーマット

YM2151ログJSONは以下の形式に従います:

```json
{
  "event_count": 50,
  "events": [
    {"time": 0, "addr": "0x08", "data": "0x00"},
    ...
  ]
}
```

各フィールドの意味:
- `time`: サンプル時刻（整数、55930 Hzサンプルレートでの値）
- `addr`: YM2151レジスタアドレス（16進数文字列）
- `data`: 書き込むデータ（16進数文字列）

## 開発

### テストの実行

```bash
python -m pytest tests/ -v
```

### プロジェクト構造

```
smf-to-ym2151log/
├── src/
│   ├── __init__.py
│   ├── midi_parser.py       # パスA: MIDIからイベントへ
│   ├── midi_utils.py        # MIDIユーティリティ関数
│   └── ym2151_converter.py  # パスB: イベントからYM2151ログへ
├── tests/
│   ├── __init__.py
│   ├── test_midi_utils.py
│   └── test_ym2151_converter.py
├── smf_to_ym2151log.py      # メインスクリプト
├── create_test_midi.py      # テストMIDIファイル生成器
└── requirements.txt
```

## 使用ライブラリ

- **mido**: MIDIファイルの解析と操作

## ライセンス

[LICENSE](LICENSE) ファイルを参照してください。

※英語版README.mdは、README.ja.mdを元にGeminiの翻訳でGitHub Actionsにより自動生成しています
