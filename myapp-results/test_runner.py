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
        os.system('mkdir {}'.format(cls.test_dir))
        runner.main(['command', '--output_dir', cls.test_dir,'examples/results.json'])

    def test_experiments(self):
        assert_equals(self.record_count('experiments.csv'), 3)
        assert_equals(self.field_counts('experiments.csv'), [108, 108, 108])

    def test_common_stages(self):
        assert_equals(self.record_count('stages.csv'), 15)
        assert_equals(self.field_counts('stages.csv'), [4] * 15)

    def test_individual_stages(self):
        table = [
            ['introduction', 3, 8],
            ['questions_begining', 3, 7],
            ['present_past_future', 3, 16],
            ['seasons_of_year', 3, 24],
            ['parts_of_day', 3, 13],
            ['days_of_week', 3, 32],
            ['timeline', 2, 15],
            ['questions_ending', 2, 9]
        ]

        for stage_name, rows, columns in table:
            file_name = 'stage_{}.csv'.format(stage_name)
            print(file_name)
            assert_equals(self.record_count(file_name), rows)
            assert_equals(self.field_counts(file_name), [columns] * rows)

    @classmethod
    def teardown_class(cls):
        os.system('rm -rf {}'.format(cls.test_dir))