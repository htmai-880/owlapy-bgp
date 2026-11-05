from typing import Any

import jpype
import pandas as pd
from owlapy.owl_ontology import SyncOntology

from owlapy_bgp.utils import startJVMWithBGP


class BGPDataSet:
    def __init__(self, ontology: SyncOntology | str):
        # noinspection PyUnresolvedReferences
        from org.semanticweb.sparql.arq import OWLOntologyDataSet

        if isinstance(ontology, str):
            # This is a path.
            from pathlib import Path

            from java.io import File

            if not Path(ontology).exists():
                raise FileNotFoundError(f"Ontology file not found: {ontology}")

            j_file = File(ontology)
            self._j_bgp_dataset = OWLOntologyDataSet(j_file, None)
        else:
            self.ontology = ontology
            self._j_bgp_dataset = OWLOntologyDataSet(
                self.ontology.get_owlapi_ontology(), None
            )

    def get_j_bgp_dataset(self) -> Any:
        """Return the underlying Java OWLOntologyDataSet object."""
        return self._j_bgp_dataset


class QueryExecutor:
    def __init__(self):
        if not jpype.isJVMStarted():
            startJVMWithBGP()

        # noinspection PyUnresolvedReferences
        from org.semanticweb.sparql import OWLReasonerSPARQLEngine

        # noinspection PyUnresolvedReferences
        # from org.semanticweb.sparql.bgpevaluation.monitor import MinimalPrintingMonitor

        self._j_bgp_engine = OWLReasonerSPARQLEngine()

    def execute_query(self, query: str, dataset: BGPDataSet) -> pd.DataFrame:
        """
        Execute a BGP query on the ontology.
        The query should include all the necessary prefixes and be in a valid SPARQL format.

        :param query: The BGP query string to be executed.
        :param dataset: The BGPDataSet containing the ontology and data.
        :return: A ResultSet containing the results of the query.
        """
        # # noinspection PyUnresolvedReferences
        # from com.hp.hpl.jena.query import ResultSet

        # noinspection PyUnresolvedReferences
        from com.hp.hpl.jena.query import ResultSetFormatter

        try:
            results = self._j_bgp_engine.execQuery(query, dataset.get_j_bgp_dataset())
            array_list = ResultSetFormatter.toList(results)
            j_result_vars = results.getResultVars()
            column_names = [str(var) for var in j_result_vars]

            results_list = []
            for j_result in array_list:
                result_dict = {}
                for var in column_names:
                    result_dict[var] = str(j_result.get(var))
                results_list.append(result_dict)
            return pd.DataFrame(results_list, columns=column_names)
        except (
            Exception
        ) as exc:  # noqa: BLE001 - Java execution can raise many runtime exceptions.
            raise RuntimeError("An error occurred while executing the query.") from exc
