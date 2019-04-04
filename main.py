import os
import shutil
import markdown
import configparser
import numpy
import lxml.html as html
import lxml.html.builder as builder
import dateparser


class Post:
    def __init__(self, id, text):
        md = markdown.Markdown(extensions=['mdx_math', 'meta'])
        self.id = id
        self.content = md.convert(text)
        self.title = md.Meta['title'][0]
        self.summary = md.Meta['summary'][0]
        self.date = dateparser.parse(md.Meta['date'][0])
        


def load_posts():
    p_list = []
    for root, dirs, files in os.walk("posts"):
        for name in dirs:
            input = open(os.path.join(root, name, "index.md"), "r")
            p_list.append(Post(name, input.read()))
        break
    p_list.sort(key=lambda p: p.date)
    return p_list

def make_head():
    head = [
        builder.BASE(href="http://localhost/my_site/docs/"),
        builder.META(charset="utf-8"),
        builder.TITLE("Author Name"),
        builder.META(name="viewport", content = "width=device-width, initial-scale=1"),
        builder.SCRIPT("", type="text/javascript", src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js",async="async"),
        builder.SCRIPT("MathJax.Hub.Config({" +
            "config: [\"MMLorHTML.js\"], "+
            "jax: [\"input/TeX\", \"output/HTML-CSS\", \"output/NativeMML\"], "+
            "extensions: [\"MathMenu.js\", \"MathZoom.js\"]});",
            type="text/x-mathjax-config"),
        builder.SCRIPT("", src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"),
        #builder.SCRIPT("", src="js/jquery.waypoints.min.js"),
        #builder.SCRIPT("", src="js/jquery.scrollTo.min.js"),
        builder.LINK(rel="stylesheet",
            href="https://use.fontawesome.com/releases/v5.8.1/css/all.css",
            integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf",
            crossorigin="anonymous")
    ]

    return head
def make_menu():
    menu = builder.UL(
        builder.LI(builder.A(builder.I("", builder.CLASS("fas fa-bars")), href=""), builder.CLASS("menu-button")),
        builder.LI(builder.A(builder.B("Author Name"), href="index.html"), builder.CLASS("menu-title")),
        builder.LI(builder.A(builder.B("Home"), href="index.html#home.page-section"), builder.CLASS("menu-item")),
        builder.LI(builder.A(builder.B("Posts"), href="index.html#posts.page-section"), builder.CLASS("menu-item")),
        builder.LI(builder.A(builder.B("Papers"), href="index.html#papers.page-section"), builder.CLASS("menu-item")),
        builder.LI(builder.A(builder.B("Contact"), href="index.html#contact.page-section"), builder.CLASS("menu-item")),
        builder.CLASS("menu")
    )
    return menu

def make_short_posts(p_list):
    tag_list = []
    for post in p_list:
        tag_list.append(builder.DIV(
            builder.H1(
                builder.A(post.title, href="posts/" + post.id + ".html"),
                builder.CLASS("post-title")
            ),
            builder.P(post.summary),
            builder.DIV(post.date.strftime("%d %b %Y, %H:%M"), builder.CLASS("post-date")),
            builder.CLASS("post-container")))
    return tag_list



def gen_index(p_list):
    index = builder.HTML(
        builder.HEAD(*make_head()),
        builder.BODY(make_menu(), builder.DIV(*make_short_posts(p_list)))
    )

    print(html.etree.tostring(index, pretty_print=True).decode("utf-8"), file=open("docs/index.html", "w"))

def gen_posts(p_list):
    for post in p_list:
        html_content = builder.DIV(
            builder.H1(post.title),
            builder.DIV(post.date.strftime("%d %B %Y, %H:%M")),
            builder.DIV(html.fromstring(post.content))
        )

        page = builder.HTML(
            builder.HEAD(*make_head()),
            builder.BODY(make_menu(), html_content)
        )
        print(html.etree.tostring(page, pretty_print=True).decode("utf-8"), file=open("docs/posts/" + post.id + ".html", "w"))


if os.path.exists("docs"):
        shutil.rmtree("docs")

os.mkdir("docs")
os.mkdir("docs/posts")


post_list = load_posts()

gen_index(post_list)
gen_posts(post_list)




