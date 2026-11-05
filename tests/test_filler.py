"""Unit tests for retrieving filler-defined classes using the owlapy-bgp package."""

from pathlib import Path

import pytest
from owlapy.owl_ontology import SyncOntology

from owlapy_bgp.engine import BGPDataSet, QueryExecutor
from owlapy_bgp.utils import startJVMWithBGP

startJVMWithBGP()  # Start the JVM with the necessary classpath for owlapy-bgp

## Download
if not Path("tests/data/pizza.owl").exists():
    url = "https://raw.githubusercontent.com/iliannakollia/owl-bgp/refs/heads/master/test/org/semanticweb/sparql/owlbgp/evaluation/ontologies/pizza.owl"
    import requests

    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the download failed
    Path("tests/data").mkdir(parents=True, exist_ok=True)
    with open("tests/data/pizza.owl", "wb") as f:
        f.write(response.content)


def test_find_file():
    # The BGPDataSet class should be able to find the pizza ontology file if it exists
    # if the ontology does not exist then it should raise a FileNotFoundError
    path_to_pizza_ontology = Path("tests/data/pizza.owl").resolve()
    BGPDataSet(str(path_to_pizza_ontology))

    non_existent_path = Path("tests/data/non_existent.owl").resolve()
    with pytest.raises(FileNotFoundError):
        BGPDataSet(str(non_existent_path))


def test_bgp_query_execution():
    # Load the pizza ontology

    path_to_pizza_ontology = Path("tests/data/pizza.owl").resolve()
    pizza_ontology = SyncOntology(str(path_to_pizza_ontology), load=True)
    # Create a BGPDataSet from the ontology
    # dataset = BGPDataSet(str(path_to_pizza_ontology))
    dataset = BGPDataSet(pizza_ontology)
    # Execute the query
    executor = QueryExecutor()

    # Execute a simple query
    query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX pizza: <http://www.co-ode.org/ontologies/pizza/pizza.owl#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?meat_topping WHERE { 
  ?meat_topping rdfs:subClassOf pizza:MeatTopping .
}"""

    results = executor.execute_query(query, dataset)
    assert results is not None, "The query execution should return results."
    print("Query Results:\n", results)

    query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX pizza: <http://www.co-ode.org/ontologies/pizza/pizza.owl#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?topping WHERE { 
  pizza:American rdfs:subClassOf [ a owl:Restriction ; 
                                   owl:onProperty pizza:hasTopping ; 
                                   owl:someValuesFrom ?topping ] . 
  ?topping rdfs:subClassOf pizza:MeatTopping . 
}"""
    results = executor.execute_query(query, dataset)
    assert results is not None, "The query execution should return results."
    print("Query Results:\n", results)
