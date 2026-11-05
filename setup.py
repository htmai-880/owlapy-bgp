from setuptools import find_packages, setup

setup(
    name="owlapy-bgp",
    version="0.1.1",
    description="Additional package for OWLAPY to execute BGP queries on SyncOntology.",
    packages=find_packages(),
    install_requires=[
        "owlapy>=1.6.7",
        "JPype1>=1.5.0",
        "pandas",
    ],
    package_data={
        "owlapy_bgp": ["extra_jar_dependencies/*.jar"],
    },
    include_package_data=True,
)
