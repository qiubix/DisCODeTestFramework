from hamcrest import *
from subprocess import call
from os.path import isfile
import unittest

from ComponentTester import ComponentTester


class TestComponentTester(unittest.TestCase):
    def setUp(self):
        self.defaultFileName = 'test_tasks/test_task.xml'
        if isfile(self.defaultFileName):
            call(['rm', self.defaultFileName])

    def test_component_tester_running(self):
        assert_that(ComponentTester(), is_not(None))

    def test_should_save_to_default_file_on_init(self):
        tester = ComponentTester()

        assert_that(isfile(self.defaultFileName), is_(True))

    def test_should_create_task_template_on_init(self):
        tester = ComponentTester()

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, starts_with('<Task>'))
        assert_that(contents, ends_with('</Task>\n'))
        assert_that(contents, contains_string('<Subtasks>'))
        assert_that(contents, contains_string('</Subtasks>'))
        assert_that(contents, contains_string('<Subtask name="Main"/>'))
        assert_that(contents, contains_string('<DataStreams/>'))

    @unittest.skip
    def test_should_create_task_with_default_executor_on_init(self):
        tester = ComponentTester()

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, contains_string('<Executor name="Processing" period="1"/>'))

    def test_should_add_proper_component_to_task(self):
        tester = ComponentTester()
        tester.setComponent('Summator', 'CvBasic:Sum')

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, contains_string('<Component bump="0" name="Summator" priority="1" type="CvBasic:Sum"/>'))

    def test_should_add_generator_to_components(self):
        tester = ComponentTester()
        tester.addGenerator('SampleGenerators:CvMatGenerator')

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, contains_string(
            '<Component bump="0" name="Generator" priority="1" type="SampleGenerators:CvMatGenerator"/>'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
