import runner
import os
from nose.tools import assert_equals
import csv


class TestRunner:
    test_dir = 'output_test'

    def lines_for(self, file_name):
        fp = open('{}/{}'.format(self.test_dir, file_name))
        records = list(csv.reader(fp))
        return records

    def record_count(self, file_name):
        return len(self.lines_for(file_name))

    def field_counts(self, file_name):
        records = self.lines_for(file_name)
        return [len(col) for col in records]

    @classmethod
    def setup_class(cls):
        runner.main(['command', '--output_dir', cls.test_dir,'examples/results.json'])

    def test_experiments(self):
        assert_equals(self.record_count('experiments_full/data.csv'), 3)
        assert_equals(self.field_counts('experiments_full/data.csv'), [477] * 3)

    def test_common_stages(self):
        assert_equals(self.record_count('stages_summary/data.csv'), 15)
        assert_equals(self.field_counts('stages_summary/data.csv'), [5] * 15)

    def test_individual_stages(self):
        table = [
            ['introduction', 3, 8],
            ['questions_begining', 3, 7],
            ['present_past_future', 3, 78],
            ['seasons_of_year', 3, 100],
            ['parts_of_day', 3, 64],
            ['days_of_week', 3, 157],
            ['timeline', 2, 55],
            ['questions_ending', 2, 10]
        ]

        for stage_name, rows, columns in table:
            file_name = 'individual_stages/{}.csv'.format(stage_name)
            print(file_name)
            assert_equals(self.record_count(file_name), rows)
            assert_equals(self.field_counts(file_name), [columns] * rows)

    def test_individual_stages_long(self):
        table = [
            ['present_past_future', 7, 22],
            ['seasons_of_year', 9, 23],
            ['parts_of_day', 7, 18],
            ['days_of_week', 15, 22],
            ['timeline', 10, 7],
        ]

        for stage_name, rows, columns in table:
            file_name = 'individual_stages_long/{}.csv'.format(stage_name)
            print(file_name)
            assert_equals(self.record_count(file_name), rows)
            assert_equals(self.field_counts(file_name), [columns] * rows)

    @classmethod
    def teardown_class(cls):
        os.system('rm -rf {}'.format(cls.test_dir))
