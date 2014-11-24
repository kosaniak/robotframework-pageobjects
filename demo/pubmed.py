from robotpageobjects import Page, robot_alias
from robot.utils import asserts


class PubmedHomePage(Page):
    """ Models the Pubmed home page at:
        HOST://ncbi.nlm.nih.gov/pubmed"""

    name = "Pubmed"
    uri = "/pubmed"

    selectors = {
        "search input": "id=term",
        "search button": "id=search",
    }


    @robot_alias("type_in__name__search_box")
    def type_in_search_box(self, txt):
        self.input_text("search input", txt)
        return self

    @robot_alias("click__name__search_button")
    def click_search_button(self):
        self.click_button("search button")
        return PubmedDocsumPage()

    @robot_alias("search__name__for")
    def search_for(self, term):
        self.type_in_search_box(term)
        return self.click_search_button()


class PubmedDocsumPage(Page):
    """Models a Pubmed search result page. For example:
    http://www.ncbi.nlm.nih.gov/pubmed?term=cat """

    uri_template = "/pubmed/?term={term}"

    selectors = {
        "nth result link": "xpath=(//div[@class='rslt'])[{n}]/p/a",
    }

    @robot_alias("click_result_on__name__")
    def click_result(self, i):
        locator = self.resolve_selector("nth result link", n=int(i))
        self.click_link(locator)
        return PubmedArticlePage()

class PubmedArticlePage(Page):

    uri_template = "/pubmed/{article_id}"

    @robot_alias("__name__body_should_contain")
    def body_should_contain(self, str, ignore_case=True):
        ref_str = str.lower() if ignore_case else str
        ref_str = ref_str.encode("utf-8")
        body_txt = self.get_text("css=body").encode("utf-8").lower()
        asserts.assert_true(ref_str in body_txt, "body text does not contain %s" %ref_str)
        return self
