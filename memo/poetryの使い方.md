---
title: Poetryをサクッと使い始めてみる
tags: Python Poetry
author: ksato9700
slide: false
---

## はじめに

以前、[pyenvとpyenv-virtualenvの自分流使い方](https://qiita.com/ksato9700/items/5d9eba10fe6b8e064178)という記事を書きました。その終わりの部分で「pyenv-virtualenv+pipをpoetryで置き換えられるんじゃないかな」と書いていたのですが、実際に試してみた結果をご紹介したいと思います。結論から言うと、pyenv-virtualenvとpipは使わなくなりました（笑）

## Poetryとは

[Poetry](https://python-poetry.org/)はPythonのパッケージマネージャの一つです。v1.0になったのが2019年末なのでまだまだ新しいツールです。pipと同じようにパッケージを[pypi](https://pypi.org/)などからダウンロードしてきてインストールすることができますが、それに加えて次のようなこともできます。

- パッケージ管理ファイルの生成・変更
- インストールされているパッケージのアップデート
- プロジェクトごとの仮想環境のセットアップ
- などなど...

他の言語だと、`npm` `yarn`（JavaScript）や`cargo`（Rust）などのパッケージマネージャーがありますが、それらと同等のものがようやくPythonにも来たという感じです。

Poetryはそのように多機能であるわけですが、その裏返しとして「コマンドがたくさんあって難しそう」とか「自分はpipで困ってないし、`requirements.txt`を自分でコントロールするのが好き」と言う方が少なからずいるかと思います。自分もその一人でしたが、実際使ってみると楽になる部分が多くあることに気が付きました。自分もまだ使い始めたばかりで全ての機能を使っているわけではないですが、それでもpipとpyenv-virtualenvを置き換えられると思ったので、とりあえず始めてみたい方のために、基本機能に絞って使い方をご紹介します。

## Poetryのインストール

Mac、Linux、Windows(Bash)上でのインストールは次の一行でいけます。

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

（Windows（Powershell）での導入方法は[ここ](https://python-poetry.org/docs/#windows-powershell-install-instructions)にかかれているのですが、私はMacを使っているので残念ながら試せていません...）

## Poetryを使う

利用する際の流れはこんな感じになります。

1. Pythonのセットアップ
1. プロジェクトのセットアップ
1. 仮想環境のセットアップ
1. 依存パッケージの追加
1. 仮想環境で実行

### 1. Pythonのセットアップ

PoetryのインストールにPythonが必要なので既に入っている前提ですが、特定のバージョンを使いたい時にはpyenvを使ってインストールしておきます。pyenvのインストール方法は[ここ](https://qiita.com/ksato9700/items/5d9eba10fe6b8e064178#%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)を参照して下さい（pyenv-virtualenvは不要）。その上で、特定のバージョンのpythonを入れるには以下のようにします。

```sh
# インストールされているバージョンを確認
pyenv versions 

# インストール可能なバージョンを表示
pyenv install --list

# 指定したバージョンをインストール
pyenv install <python-version>

# グローバルなデフォルトを指定したバージョンに変更
pyenv global <python-version>
```



### 2. プロジェクトのセットアップ

使いたいバージョンのPythonがセットアップされたら、次にPoetryのプロジェクト（パッケージ）をセットアップします。これには「新規に立ち上げる場合」と「既にあるプロジェクトをpoetry管理下に置く場合」の二通りあります。

#### 新規に立ち上げる場合

まっさらな状態から新たにプロジェクトを作る場合は `poetry new`を使います。

```sh
poetry new <project-name>
```

そうすると、`<project-name>`ディレクトリ配下にファイルが幾つかできます。以下の例では "project_abc"というパッケージ名をつけています。

```
project_abc
├── README.rst
├── project_abc
│   └── __init__.py
├── pyproject.toml
└── tests
    ├── __init__.py
    └── test_project_abc.py
```

Pythonパッケージの標準的なディレクトリ構成で自動的にファイルを作ってくれています。

- **REAME.rst** ... そのプロジェクトの概要を記述するファイル。GitHubだとトップページにこれを表示してくれますね。中身は空ですが、拡張子が `.rst`になっていて [reStructuredText](https://docutils.sourceforge.io/rst.html) というマークアップ言語で書くことが期待されています。reStructuredTextはMarkdownが流行る前からPython系のドキュメントで使われていた形式ですが、Markdownの方が得意という方はこれを `README.md`に変えてしまっても良いかなと思います。なお、GitHubでは`README.rst`だったとしても問題なくレンダリングしてくれます。
- **project_abc/**... `project_abc/`はこのパッケージのpythonソースコードを格納するディレクトリで、その元締めとして `__init__.py`が作られています。ここではバージョンの定義だけがされています。
- **pyproject.toml** ... Poetryプロジェクトに関するメタデータや依存関係を記述するためのファイルです。[TOML](https://toml.io/en/)という形式で書かれています。これに関しては後述します。
- **tests/** ... `tests/`はユニットテストを格納するディレクトリで、`__init__.py`とバージョン番号を確認する簡単なテストが `test_project_abc.py`に書かれています。

#### 既にあるプロジェクトをpoetry管理下に置く場合

既にソースコードを書き始めてしまった場合、あるいは既にpipなどで管理しているPythonのプロジェクトでpoetryを使い始める場合には `poetry init`を使います。

```sh
cd project_xyz
poetry init
```

そうすると、対話的に色々と訊かれていくのでそれに答えていきます。英語ですがそれほど難しくないと思います。質問の後に`[]`でデフォルト値が書かれているのでそれで良い場合は単にEnterを押すだけです。だいたいこんな感じ。

```sh
Package name [project_xyz]:
Version [0.1.0]:
Description []:
Author [John Doe <johnd@example.com>, n to skip]:
License []:
Compatible Python versions [^3.9]:
```

上から、パッケージ名、バージョン、説明文、著者、ライセンス、互換性のあるPythonのバージョン、です。

そしてこの後に "Would you like to define your main dependencies interactively? (yes/no) [yes]"と訊かれるのですが、これは「依存関係を今ここで登録する？」という問いですね。あとで一つ一つ `poetry add`で追加することができるので `no`でも良いのですが、`yes`してみると、指定の仕方の説明が出てきたり、名前を入れると似たような名前のものをサジェストしてくれたり、一回やってみると面白いかも知れません。追加するものがない時には何も入れずにEnter押すと次に進みます。

で終わりかと思いきや、また "Would you like to define your development dependencies interactively? (yes/no) [yes]" と訊かれます。あれ、また同じこと訊かれている？と思うのですが、よく見るとさっきのは "main dependencies"でこちらは "development dependencies"です。何が違うかと言うと、mainの方はそのパッケージが動作するのに必要な依存パッケージを登録し、developmentの方は本番動作に必要ないけど開発する時には必要なパッケージを登録します。後者は、例えば`pytest`などのテストフレームワークや `flake8`, `black`などのリンター、フォーマッターなどですね。パッケージを使うだけの人にとってはそれらのフレームワークやツールは不要なので、developmentの依存関係として登録しておいて、インストール時にそれを省ける様になっています。

これを終えると、「これで良い？」と今まで入力したものの確認がされて、Enter押すと完了です。そして、カレントディレクトリに `pyproject.toml`ができていると思います。`init`の場合は既に色々作られているという前提なので`new`の時のような他のファイルは作られません。

#### pyproject.toml

`poetry new`や`poetry init`した時にできる`pyproject.toml`ですが、これは[PEP-518](https://www.python.org/dev/peps/pep-0518/)で定義されたPython標準のフォーマットです。そのため、poetryだけではなく、例えば最近のpipでもこのファイルを参照してパッケージのビルド・インストールができたりしますし、今後対応するツールがもっと出てくるでしょう。これまでは `setup.py`と`requirements.txt`に同じような情報をコピーして持たなければならなかったのが、`pyproject.toml`に集約された感じですね。

以下は生成された`pyproject.toml`の例です。

```toml
[tool.poetry]
name = "project_abc"
version = "0.1.0"
description = ""
authors = ["John Doe <johnd@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.dev-dependencies]
pytest = "^5.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

```

### 3. 仮想環境のセットアップ

前の手順でPoetryのセットアップが終わったので、次にこのプロジェクト用の仮想環境を立ち上げます。それには

```sh
poetry install
```

とします。

引数無しで起動すると、まずは `./.venv`というディレクトリ配下に仮想環境のセットアップを行い、そこに、`pyproject.toml`に書かれた依存関係（mainとdevelopmentの双方）のパッケージをインストールしていきます。先ほど、`poetry new`で作った`project_abc`で実行してみると、`pytest`がデフォルトでdevelopment依存関係に入っているので、それがインストールされたかと思います。

また、もしdevelopmentの依存関係が不要であれば、

```sh
poetry install --no-dev
```

とすることもできます。

### 4.依存パッケージの追加

`poetry new`した場合や`poetry init`で依存関係の追加をスキップした場合は、必要なパッケージの追加をする必要があります。また、開発途中で必要に応じて依存パッケージを追加することもよくあります。そんな時には`poetry add`を使います。

```sh
poetry add <package-name>
```

pip同様に指定したパッケージだけでなく、それが依存しているパッケージも合わせてインストールしてくれます。そして、`pyproject.toml`にインストールしたパッケージをバージョンとともに追加してくれます。

```sh
[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.26.0"
```

ここでバージョン番号に `^`という記号が付いていると思いますが、これは許容するバージョンの範囲を示すものです。例えば`^2.26.0`であれば、`2.26.0 <= version < 3.0.0`の範囲でアップップグレード可能ということになります。ここで用いているのは Semantic Versionという考え方で、バージョンは `major.minor.patch`という形で、`minor`と`patch`は値が上がっても後方互換性は維持するということになっています。したがって、この場合だと、`major`バージョンの`2`が維持される限りアップグレードしても問題は起こらない前提を置くことができます。このように、バージョンを範囲で指定でできるので、新しいバージョンが出る度に `pyproject.toml`を変更しなくても良いということになります。

ただ、そうすると実際に使っている依存パッケージのバージョンが曖昧になってしまうという問題があります。上の例だと、ある人は`2.26.0`を使い続け、また別の人はその後にリリースされた`2.27.0`を使っているということが起こりえます。その問題を解決するために `poetry.lock`というファイルがあります。

`poetry.lock`はpoetryが自動的に生成するファイルの一つです。実は上で `poetry install`した時に既に作られていました。ここに何が書いてあるかというと、今現在仮想環境にインストールされているパッケージのリストとそのバージョンです。`pyproject.toml`で指定されているものだけでなく、それらが依存しているパッケージも含まれています。

そして、`poetry.lock`ファイルがある場合には、`poetry install`はそちらを先に見に行きます。したがって、例えば `pyproject.toml`に`^2.26.0`と書いてあって、`poetry.lock`に `version="2.27.0"`と書いてあれば、`2.27.0`がインストールされることになります。チーム開発している場合は、`poetry.lock`をバージョン管理化に置いて、リポジトリにコミットすれば、チームメンバー全員が同じバージョンのパッケージを使って開発をすることが出来ます。

インストールされているパッケージのアップグレード（バージョンアップ）を行いたい時には `poetry update`を使います。

```sh
poetry update --dry-run
```

とするとアップグレードされるパッケージがわかるので、それを確認した上で

```sh
poetry update
```

すると実際にアップグレードが行われます。なお、`poetry update`した時に変更されるのは`poetry.lock`だけで `pyproject.toml`はそのままです。新しいバージョンの新機能を使うなどの場合は`pyproject.toml`を手動で修正してして依存するバージョンを変える必要があります。

### 5. 仮想環境で実行

必要な依存パッケージの追加ができたら実行です。仮想環境でpythonのプログラムを実行するには

```sh
poetry run python <python-file>
```

あるいは

```sh
poetry shell
python <python-file>
```

とします。前者は実行のたびに仮想環境に入り、終わったら元の世界に戻ってくるという実行方法。後者は一旦仮想世界に入って、行きっぱなしのまま実行するという方法です。

なお、仮想環境ではpythonだけでなく、依存関係で追加したパッケージに含まれるコマンドも実行できます。例えば、`project_abc`で`pytest`によるユニットテストを実行するには、

```sh
poetry run pytest
```

あるいは

```sh
poetry shell
pytest
```

とすれば良いです。

## まとめ

Poetryを使い始めてみる方法について書いてみました。Poetryにはまだまだ他にたくさん機能があるのですが、今回は基本的な機能に絞ってみました。私自身もまだ使いこなしているとは言えないので、より便利な使い方が見つかったらまた記事にしてみたいと思います。
