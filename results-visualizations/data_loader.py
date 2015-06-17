from stages import all_stages


class DataLoader:
    def __init__(self, tables_dir, clusters_dir):
        stages = [s.stage_name() for s in all_stages()]

