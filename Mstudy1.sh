# 仮想環境の作成とアクティベート
python -m venv myenv
source myenv/bin/activate

# 必要なパッケージのインストール
pip install -r requirements.txt

python NYCTaxi0.py

python NYCTaxi1.py

python NYCHex0.py

# 仮想環境のデアクティベート
deactivate