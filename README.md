# owlapy-bgp

A small OWLAPY add-on for running Basic Graph Pattern (BGP) SPARQL queries against an ontology loaded through `SyncOntology`.

This package bridges OWLAPY with a Java-backed BGP engine, letting you execute queries and get results as a Pandas DataFrame.

> The Java BGP software used here is based on the project at https://github.com/htmai-880/owl-bgp.

## What this package does

- Loads an OWL ontology in OWLAPY
- Wraps it into a dataset object compatible with the Java BGP engine
- Executes SPARQL BGP queries through `QueryExecutor`
- Returns results as a Pandas DataFrame for easy inspection and downstream processing

## Installation

From a local checkout:

```bash
python -m pip install -e .
```

If you are using this project as a dependency in another environment, install it normally via pip in that environment.

## Quick start

```python
from pathlib import Path

from owlapy.owl_ontology import SyncOntology

from owlapy_bgp.engine import BGPDataSet, QueryExecutor
from owlapy_bgp.utils import startJVMWithBGP

# Start the Java JVM with the owl-bgp dependency included
startJVMWithBGP()

ontology_path = Path("tests/data/pizza.owl").resolve()
ontology = SyncOntology(str(ontology_path), load=True)

dataset = BGPDataSet(ontology)
executor = QueryExecutor()

query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX pizza: <http://www.co-ode.org/ontologies/pizza/pizza.owl#>
SELECT ?meat_topping WHERE {
  ?meat_topping rdfs:subClassOf pizza:MeatTopping .
}
"""

results = executor.execute_query(query, dataset)
print(results)
```

This returns a Pandas DataFrame whose columns match the query variables.

## Using a file path instead of an ontology object

You can also create the dataset directly from an ontology file without constructing the `SyncOntology` object first:

```python
from owlapy_bgp.engine import BGPDataSet, QueryExecutor
from owlapy_bgp.utils import startJVMWithBGP

startJVMWithBGP()

ontology_path = "tests/data/pizza.owl"
dataset = BGPDataSet(ontology_path)
executor = QueryExecutor()

query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX pizza: <http://www.co-ode.org/ontologies/pizza/pizza.owl#>
SELECT ?topping WHERE {
  ?topping rdfs:subClassOf pizza:MeatTopping .
}
"""

print(executor.execute_query(query, dataset))
```

## Notes for efficient use

- Call `startJVMWithBGP()` once at startup if you want explicit control over the JVM initialization.
- `QueryExecutor` will start the JVM automatically if it has not already started.
- Keep your SPARQL queries fully prefixed and valid; the Java backend expects standard SPARQL syntax.
- Use the returned DataFrame directly for filtering, analysis, or exporting to CSV/Parquet.

## Example with a more complex query

```python
query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX pizza: <http://www.co-ode.org/ontologies/pizza/pizza.owl#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?topping WHERE {
  pizza:American rdfs:subClassOf [ a owl:Restriction ;
                                   owl:onProperty pizza:hasTopping ;
                                   owl:someValuesFrom ?topping ] .
  ?topping rdfs:subClassOf pizza:MeatTopping .
}
"""

results = executor.execute_query(query, dataset)
print(results)
```

## Upstream Java BGP source

This project relies on the Java BGP implementation maintained in:

https://github.com/htmai-880/owl-bgp

The Python package here wraps that Java backend for integration with OWLAPY and Pandas-based workflows.

## License

See [LICENSE](LICENSE) for details.
