# SGWPoC-MiX
条件の異なるファイルをミックスしてリードするテストツール


## 前提
- windows platform
- python3 [https://www.python.org/downloads/release/python-381/](https://www.python.org/downloads/release/python-381/)
- git [git for windows](https://gitforwindows.org/)

# 準備
## 環境
```sh
git clone https://github.com/Noppy/SGWPoC-MiX.git
cd SGWPoC-MiX.git
```
## Associatedカテゴリー
指定したディレクトリのファイルから自動生成するので、個別作成不要

## Unassociatedカテゴリー
下記のようなCSVファイルを事前準備しておく。
```csv
"最初のコピーの元ファイル", "2番目のコピーの元ファイル", "コピー先ディレクトリ"
"F:/20150103/0000/test-001000KB_000300.dat","F:/20150103/0000/test-001000KB_000800.dat","D:/"
"F:/20150103/0001/test-001000KB_000301.dat","F:/20150103/0001/test-001000KB_000801.dat","D:/"
"F:/20150103/0002/test-001000KB_000302.dat","F:/20150103/0002/test-001000KB_000802.dat","D:/"
```

## 実行
### ファイルサーバ初期化
キャッシュされないよう、ファイルサーバの既存設定をクリアし再セットアップをします。

### 検証実施
```sh
python.exe .\Execute_MixTest.py --dest D:\ --PreReadDir F:\20150101\ .\UnassociatedFiles.csv --Times 3 --Interval 9
```

## 実行結果
実行結果は、下記に記録されます。
- ResultsSummary.csv : 実行の結果サマリーが記録されます。
- ResultsDetail__XXXX_associate_YYYYMMDD_HHMMSS.csv :   インベントリ登録済みファイルコピータスクの実行詳細結果(XXXXはunassociate実行間隔)
- ResultsDetail__XXXX_unassociate_YYYYMMDD_HHMMSS.csv : インベントリ未登録ファイルコピータスクの実行詳細結果(XXXXはunassociate実行間隔)

### ResultsSummary.csvのフィールド
- 全体の実行時間(sec)
- 全体の開始時間
- 全体の終了時間
- 成功したタスク数
- 失敗したタスク数
- 結果不明なタスク数
- 実行結果のタスク合計数

### ResultsDetail__XXXX_YYYYMMDD_HHMMSS.csvのフィールド
- 最初のコピー元ファイル
- 2番目のコピー元ファイル
- コピー先
- タスクの開始時間
- テストプログラム(親プログラム)開始時間を基準とした、最初のファイルのコピー開始までの時間(msec)
- テストプログラム(親プログラム)開始時間を基準とした、最初のファイルのコピー完了までの時間(msec)
- テストプログラム(親プログラム)開始時間を基準とした、2番目のファイルのコピー完了までの時間(msec)
- タスクの結果(Success or Failed)
- タスクがFailedになった時の、エラーメッセージ
