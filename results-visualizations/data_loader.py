import stages
import csv


class DataLoader:
    def __init__(self, tables_dir, clusters_dir):
        self.results = {}
        for stage_class in stages.all_stages():
            stage_name = stage_class.stage_name()

            rows = self.read_with_names('{}/{}.csv'.format(tables_dir, stage_name))
            stage_objects = {row['experiment_id']: stage_class(row) for row in rows}

            rows = self.read_with_names('{}/{}.csv'.format(clusters_dir, stage_name))
            cluster_rows = {row['experiment_id']: row for row in rows}

            stage_results = {}
            for k in cluster_rows.keys():
                cluster_item = cluster_rows[k]
                cluster_id = cluster_item['cluster']
                if cluster_id not in stage_results:
                    stage_results[cluster_id] = []

                stage = stage_objects[k]
                value = {"stage": stage, "center_dist": cluster_item['center_dist']}
                stage_results[cluster_id].append(value)

            self.results[stage_name] = stage_results

    @staticmethod
    def read_with_names(csv_path):
        results = []
        with open(csv_path, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)

            for row in reader:
                named_row = {}
                for i in range(len(row)):
                    named_row[header[i]] = row[i]
                results.append(named_row)

        return results