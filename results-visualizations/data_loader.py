import stages
import csv


class DataLoader:
    def __init__(self, tables_dir, clusters_dir):
        self.results = {}
        for stage in stages.all_stages():
            stage_name = stage.stage_name()
            with open('{}/individual_stages/{}.csv'.format(tables_dir, stage_name), newline='') as f:
                reader = csv.reader(f)
                next(reader)  # skip header
                stage_objects = [stage(row) for row in reader]

            with open('{}/{}.csv'.format(clusters_dir, stage_name), newline='') as f:
                reader = csv.reader(f)
                next(reader)  # skip header
                cluster_rows = [row for row in reader]


            # create cluster objects or hash of arrays
            #self.results[stage_name] = objects

    #@staticmethod
    #def get_stage():