import serializers
import stages
import csv


def all_drivers():
    return [
        Experiments,
        CommonStages,
        IndividualStages
    ]


class Experiments:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def serialize(self, experiments):
        with open('{}/experiments.csv'.format(self.output_dir), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.get_header())
            for e in experiments:
                writer.writerow(self.get_row_for(e))

    def get_header(self):
        serializer = serializers.StageHeader()
        result = []
        for stage in stages.all_stages():
            sn = stage.stage_name()
            fields = ['duration', 'size_in_bytes'] + serializer.row_for(stage)
            fields = ["{}_{}".format(sn, f) for f in fields]
            result.extend(fields)
        return result

    def get_row_for(self, experiment):
        serializer = serializers.StageData()
        result = []
        for stageCls in stages.all_stages():
            if experiment.has_stage(stageCls):
                stage = experiment.stage_named(stageCls.stage_name())
                fields = [stage.time_duration(), stage.size_in_bytes()] + serializer.row_for(stage)
            else:
                fields = ['missing'] * (len(serializers.StageHeader().row_for(stageCls)) + 2)
            result.extend(fields)
        return result


class CommonStages:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def serialize(self, experiments):
        stgs = []
        for exp in experiments:
            stgs.extend(exp.stages())

        with open('{}/stages.csv'.format(self.output_dir), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header_serializer = serializers.StageHeader()
            data_serializer = serializers.StageData()

            writer.writerow(header_serializer.common_row())
            for s in stgs:
                writer.writerow(data_serializer.common_row_for(s))


class IndividualStages:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def serialize(self, experiments):
        stgs = []
        for exp in experiments:
            stgs.extend(exp.stages())

        writers = {}
        a_serializer = serializers.StageHeader()
        for s in stages.all_stages():
            sn = s.stage_name()
            csv_file = open('{}/stage_{}.csv'.format(self.output_dir, sn), 'w', newline='')
            csv_writer = csv.writer(csv_file)
            writers[sn] = csv_writer

            csv_writer.writerow(a_serializer.common_row() + a_serializer.row_for(s))

        a_serializer = serializers.StageData()
        for s in stgs:
            sn = s.stage_name()
            writers[sn].writerow(a_serializer.common_row_for(s) + a_serializer.row_for(s))
