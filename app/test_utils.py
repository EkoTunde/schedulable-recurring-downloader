from unittest import TestCase
from app.utils import build_instruction
from settings import SeleniumType, SeleniumBy  # , SeleniumSelectionType


class TestBuildInstruction(TestCase):

    """
    ID = 'HTML id => <tag id=$id></tag>'
    NAME = 'HTML name => <tag name=$name></tag>'
    TAG_NAME = 'HTML tag => <$tag></$tag>'
    CLASS_NAME = "HTML class => <tag class=$class></tag>"
    XPATH = "xpath"
    LINK_TEXT = 'El texto de un link HTML => <a href=...> $texto</a>'
    PARTIAL_LINK_TEXT = ('Texto en un link HTML => <a href=...>'
                         ' The quick $texto fox jumps...</a>')
    CSS_SELECTOR = "Selector CSS"
    """

    def click_by_case(self, by):
        return build_instruction(SeleniumType.CLICK, by, "test1")

    def test_1_click_by_id(self):
        by = SeleniumBy.human_text(SeleniumBy.ID)
        expected = f"Clickear el {by} llamado test1"
        self.assertEqual(
            expected,
            self.click_by_case(SeleniumBy.ID))

    def test_1_click_by_name(self):
        by = SeleniumBy.human_text(SeleniumBy.NAME)
        expected = f"Clickear el {by} llamado test1"
        self.assertEqual(
            expected,
            self.click_by_case(SeleniumBy.NAME))

    def test_1_click_by_tag_name(self):
        by = SeleniumBy.human_text(SeleniumBy.TAG_NAME)
        expected = f"Clickear el {by} llamado test1"
        self.assertEqual(
            expected,
            self.click_by_case(SeleniumBy.TAG_NAME))

    # def test_1_click(self):
    #     result = build_instruction(
    #         action: SeleniumType,
    #         by: SeleniumBy,
    #         value: str,
    #         input_text: str=None,
    #         selection_type: SeleniumSelectionType=None,
    #         select_value: str=None
    #     )
    #     self.assertEqual("Clickear el id", result)
