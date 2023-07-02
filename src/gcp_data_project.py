
from diagrams import Diagram, Cluster
from diagrams.gcp.storage import GCS
from diagrams.gcp.compute import Functions, Run, GKE
from diagrams.gcp.analytics import Dataflow
from diagrams.gcp.ml import AIPlatform

__author__ = 'psessford'


def create_diagram():
    """Create diagram and output to local file"""
    with Diagram('GCP Data Project', show=False):
        with Cluster('Tech team'):
            with Cluster('Deployed web apps'):
                gke_web_app = GKE('GKE')

        with Cluster('Data Science team'):
            gcs_data_source = GCS('GCS\nraw data')

            with Cluster('Orchestrator'):
                cloud_run_orchestrator = Run('Cloud Run')

            gcs_processed_data = GCS('GCS\nprocessed\ndata')
            gcs_ml_model = GCS('GCS\nML model')

            with Cluster('Data pipeline'):
                data_pipeline_components = [
                    ([cloud_run_orchestrator, gcs_data_source] >>
                    Dataflow('Dataflow') >> gcs_processed_data),
                    ([cloud_run_orchestrator, gcs_processed_data] >>
                    AIPlatform('AI Platform\nTraining') >> gcs_ml_model),
                ]

            (gcs_data_source >> Functions('Function\nevent-driven') >>
            cloud_run_orchestrator)

            gcs_ml_model >> gke_web_app
