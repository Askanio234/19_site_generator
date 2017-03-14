import os
import json
from jinja2 import Environment, FileSystemLoader
import markdown


CONTENT_DIR = "articles"

TEMPLATE_DIR = "templates"

SITE_DIR = "site"

CONFIG = "config.json"


def load_json(path_to_json):
    with open(path_to_json, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def load_md_file(path_to_file):
    with open(path_to_file, "r", encoding="utf-8") as md_file:
        return md_file.read()


def convert_to_html(md_text):
    md = markdown.Markdown()
    return md.convert(md_text)


def create_jinja2_environment():
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True,)
    return env


def check_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def create_html_articles(json, article_template):
    for article in json["articles"]:
        md_article_path = "{}/{}".format(CONTENT_DIR, article["source"])
        content = convert_to_html(load_md_file(md_article_path))
        article_html = article_template.render(content=content,
                                                title=article["title"])
        html_article_path = "{}/{}".format(SITE_DIR,
                                article["source"].replace(".md", ".html"))
        check_directory("{}/{}".format(SITE_DIR,
                                        article["source"].split("/")[0]))
        write_html_article(article_html, html_article_path)


def write_html_article(html_content, path_to_file):
    with open(path_to_file, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)


if __name__ == '__main__':
    json_file = load_json(CONFIG)
    articles = json_file["articles"]
    topics = json_file["topics"]
    env = create_jinja2_environment()
    article_template = env.get_template("base_article.html")
    main_page_template = env.get_template("base_main.html")
    create_html_articles(json_file, article_template)
    content_main = main_page_template.render(topics=topics, articles=articles)
    write_html_article(content_main, "{}/index.html".format(SITE_DIR))
