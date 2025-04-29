FROM python:3.11

# 作業ディレクトリを作成
WORKDIR /app

# 必要なパッケージをインストール
RUN pip install --upgrade pip
RUN pip install django==5.2

# Djangoプロジェクトをコピー
COPY sandbox/ .

# ポートを公開
EXPOSE 8000

# Django開発サーバーを起動するコマンド
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]