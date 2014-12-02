import stages

class StageHeader:
    def row_for(self, stage):
        return stage.visit_header(self)

    def common_row(self):
        return ['experiment_id', 'time_start', 'time_duration', 'size_in_bytes']

    def case_introduction(self, stage):
        return ['ip_address', 'user_agent', 'participant', 'local_id']

    def case_questions_begining(self, stage):
        return ['name', 'age', 'sex']

    def case_present_past_future(self, stage):
        return self.variables_for(stage, ['center_x', 'center_y', 'radius', 'color'])

    def case_seasons_of_year(self, stage):
        return self.variables_for(stage, ['center_x', 'center_y', 'size_x', 'size_y', 'color'])

    def case_days_of_week(self, stage):
        return self.variables_for(stage, ['center_x', 'center_y', 'size_y', 'color'])

    def case_parts_of_day(self, stage):
        return self.variables_for(stage, ['rotation', 'size', 'color'])

    def case_timeline(self, stage):
        result = ['line_rotation', 'line_length']
        result.extend(self.variables_for(stage, ['position']))
        return result

    def case_questions_ending(self, stage):
        return ['represents_time', 'cronotype', 'forced_size', 'forced_color', 'forced_position']

    @staticmethod
    def variables_for(stage, variables):
        elements = stage.stage_elements()
        return ['{}_{}'.format(var, elem) for var in variables for elem in elements]


class StageData:
    def row_for(self, stage):
        return stage.visit(self)

    def common_row_for(self, stage):
        return [stage.experiment_id(), stage.time_start(), stage.time_duration(), stage.size_in_bytes()]

    def case_introduction(self, stage):
        return [stage.ip_address(), stage.user_agent(), stage.participant(), stage.local_id()]

    def case_questions_begining(self, stage):
        return [stage.name(), stage.age(), stage.sex()]

    def case_present_past_future(self, stage):
        return self.variables_for(stage, ['center_x', 'center_y', 'radius', 'color'])

    def case_seasons_of_year(self, stage):
        return self.variables_for(stage, ['center_x', 'center_y', 'size_x', 'size_y', 'color'])

    def case_days_of_week(self, stage):
        return self.variables_for(stage, ['center_x', 'center_y', 'size_y', 'color'])

    def case_parts_of_day(self, stage):
        return self.variables_for(stage, ['rotation', 'size', 'color'])

    def case_timeline(self, stage):
        result = [stage.rotation(), stage.length()]
        result.extend(self.variables_for(stage, ['position']))
        return result

    def case_questions_ending(self, stage):
        return [
            stage.represents_time(), stage.cronotype(),
            stage.choice_size(), stage.choice_color(), stage.choice_position()
        ]

    @staticmethod
    def variables_for(stage, variables):
        elements = type(stage).stage_elements()
        return [stage.element_data(elem)[var] for var in variables for elem in elements]


class ExperimentHeader:
    def row(self):
        return [
            'id', 'num_stages', 'start_time',
            'duration', 'is_complete', 'size_in_bytes'
        ]


class ExperimentData:
    def row_for(self, experiment):
        return [
            experiment.experiment_id(), experiment.num_stages(), experiment.time_start(),
            experiment.time_duration(), experiment.is_complete(), experiment.size_in_bytes()
        ]
