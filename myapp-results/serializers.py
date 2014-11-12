class StageHeader:
    def row_for(self, stage):
        stage.visit(self)

    def common(self, stage):
        return ['experiment_id', 'time_start', 'time_duration', 'size_in_bytes']

    def case_introduction(self, stage):
        return ['ip_address', 'user_agent', 'participant', 'local_id']

    def case_questions_begining(self, stage):
        return ['name', 'age', 'sex']

    def case_present_past_future(self, stage):
        pass

    def case_seasons_of_year(self, stage):
        pass

    def case_days_of_week(self, stage):
        pass

    def case_parts_of_day(self, stage):
        pass

    def case_timeline(self, stage):
        pass

    def case_questions_ending(self, stage):
        return ['represents_time', 'cronotype', 'choice_size', 'choice_color', 'choice_position']


class StageData:
    def row_for(self, stage):
        stage.visit(self)

    def common(self, stage):
        return [stage.experiment_id(), stage.time_start(), stage.time_duration(), stage.size_in_bytes()]

    def case_introduction(self, stage):
        return [stage.ip_address(), stage.user_agent(), stage.participant(), stage.local_id()]

    def case_questions_begining(self, stage):
        return [stage.name(), stage.age(), stage.sex()]

    def case_present_past_future(self, stage):
        pass

    def case_seasons_of_year(self, stage):
        pass

    def case_days_of_week(self, stage):
        pass

    def case_parts_of_day(self, stage):
        pass

    def case_timeline(self, stage):
        pass

    def case_questions_ending(self, stage):
        return [
            stage.represents_time(), stage.cronotype(),
            stage.choice_size(), stage.choice_color(), stage.choice_position()
        ]


class ExperimentHeader:
    pass


class ExperimentData:
    pass
