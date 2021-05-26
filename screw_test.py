import requests


def detect_questions(paper: str) -> str:
    """
    Return all the detected questions from the paper
    """

    # NOTE: This function is not perfect, it returns some non-questions too. It's
    # not necessary to fix it but the program will become slightly more efficient
    # and accurate if I do so.

    questions = []
    for line in paper.splitlines():
        # If line is JUST number, then don't add it to questions.
        line = line.strip()
        if not line.isdigit() and len(line) > 0:
            questions.append(line)
    return questions


def get_ddg_urls(question: str) -> str:
    """
    Return DuckDuckGo URLs for the search query of the question.
    Supports papacambridge, physicsandmathstutor and xtremepapers.
    """
    query_ques = question.replace(" ", "+")
    urls = [
        "https://duckduckgo.com/?q=papacambridge+{}&t=hc&va=u&ia=web".format(
            query_ques
        ),
        "https://duckduckgo.com/?q=physicsandmathstutor+{}&t=hc&va=u&ia=web".format(
            query_ques
        ),
        "https://duckduckgo.com/?q=xtremepapers+{}&t=hc&va=u&ia=web".format(query_ques),
    ]
    return urls


def find_question_urls(driver, question: str) -> str:
    """
    Return URL of major question websites.
    """
    urls = []
    query_urls = get_ddg_urls(question)

    for query in query_urls:
        driver.get(query)

        # Get all website links
        question_urls = driver.find_elements_by_xpath("//a[@href]")
        for elem in question_urls:
            # Check if link contains the question website domains and if it does,
            # append the URL.
            url = elem.get_attribute("href")
            if (
                "https://pmt.physicsandmathstutor.com" in url
                or "https://pastpapers.papacambridge.com" in url
                or "https://papers.xtremepape.rs" in url
            ):
                if "QP" in url or "_qp_" in url:
                    if url.endswith(".pdf"):
                        urls.append(url)

    return urls


def find_answer(question_url: str) -> str:
    """
    Return answer link.
    """
    answer_url = None

    # Prepare mark scheme links
    if "https://pmt.physicsandmathstutor.com" in question_url:
        # This is how physicsandmathstutor organizes URL. The question paper
        # has "QP.pdf" at the end and the mark scheme paper has "MS.pdf" at the
        # end. The other parts of both URLs are the same.
        answer_url = question_url.replace("QP.pdf", "MS.pdf")
    else:
        answer_url = question_url.replace("_qp_", "_ms_")

    # Check if URL exists
    if answer_url is not None:
        site = requests.get(answer_url)
        if site.status_code == 200:
            return answer_url

    return answer_url
