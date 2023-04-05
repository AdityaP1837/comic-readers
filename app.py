from flask import Flask, render_template
import data

app = Flask(__name__)


@app.route('/')
def home():
    resource = data.Link_Gather()
    main_page_trending = resource.main_page_trending()
    latest_comics = resource.main_page_latest()
    return render_template('main-page.html', main_page_list=main_page_trending, main_page_latest=latest_comics)


@app.route('/comic-list')
def comic_list():
    comic_list_info = data.Link_Gather()
    list_details = comic_list_info.Comic_List("0")
    comic_links = list_details["comic-links"]
    list_content = list_details["list"]
    size = len(list_content)
    return render_template('comic-list.html', comic_l=comic_links, content_list=list_content, list_length=size)


@app.route('/comic-list/<alphabet>')
def comic_list_nav(alphabet):
    comic_list_info = data.Link_Gather()
    list_details = comic_list_info.Comic_List(f"{alphabet}")
    comic_links = list_details["comic-links"]
    list_content = list_details["list"]
    size = len(list_content)
    return render_template('comic-list.html', comic_l=comic_links, content_list=list_content, list_length=size)


@app.route('/comic-page/<pagelink>')
def comic_page(pagelink):
    full_info = data.Link_Gather()
    full_info_list = full_info.comic_page(page_title=pagelink)
    return render_template('comic-page.html', info_list=full_info_list)


@app.route('/reading-page/<title>/<issue>/<id>')
def reading_page(title, issue, id):
    resource = data.Link_Gather()
    issue_info = resource.reading_page(
        issue_title=title, issue_num=issue, issue_id=id)
    return render_template('reading-page.html', page_info_list=issue_info)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
