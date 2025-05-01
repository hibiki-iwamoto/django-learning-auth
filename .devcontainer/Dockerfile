# .devcontainer/Dockerfile
# ベースイメージの選択 (devcontainer 標準の Python イメージを使うのが一般的)
# ARG でバージョンを受け取れるようにする
ARG PYTHON_VERSION=3.11
FROM mcr.microsoft.com/devcontainers/python:${PYTHON_VERSION}

# 開発に必要なツールと言語サーバーをインストール (必要に応じて追加)
# postgresql-client は psql コマンドを使う場合に便利
# RUN sudo apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && sudo apt-get -y install --no-install-recommends postgresql-client curl \
#     && sudo apt-get autoremove -y && sudo apt-get clean -y && sudo rm -rf /var/lib/apt/lists/*
RUN sudo apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && sudo apt-get -y install --no-install-recommends curl \
    && sudo apt-get autoremove -y && sudo apt-get clean -y && sudo rm -rf /var/lib/apt/lists/*

# Poetry のインストール
USER vscode # 非rootユーザーでインストールすることが推奨される場合が多い
ENV POETRY_HOME="/home/vscode/.local" \
    PATH="/home/vscode/.local/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

# Poetry の設定: コンテナ内に仮想環境を作成しない (コンテナ自体が環境のため)
RUN poetry config virtualenvs.create false

# アプリケーションのコードをコピーする前に依存関係をインストールすると、
# コード変更時に毎回依存関係を再インストールするのを避け、ビルドキャッシュを効率化できる
WORKDIR /tmp/poetry_install
COPY pyproject.toml poetry.lock* ./

# 依存関係のインストール (--no-root は通常ライブラリ開発用だが、アプリでも問題ないことが多い)
# もしプロジェクト自体をインストールしたい場合は --no-root を外す
RUN poetry install --no-interaction --no-ansi --no-root

# ワークスペースに移動し、一時ファイルをクリーンアップ
WORKDIR /workspaces/${localWorkspaceFolderBasename}
RUN rm -rf /tmp/poetry_install
