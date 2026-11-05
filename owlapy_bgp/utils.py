"""Utility helpers for starting the Java JVM with the owlapy-bgp classpath."""

from importlib import resources

from owlapy.static_funcs import startJVM


def path_to_owlapy_bgp_jar() -> str:
    """Return the filesystem path to the owlapy-bgp JAR file."""
    jar_path = resources.files("owlapy_bgp").joinpath(
        "extra_jar_dependencies",
        "owl-bgp-0.1.0-SNAPSHOT.jar",
    )
    if not jar_path.is_file():
        raise FileNotFoundError(f"owlapy-bgp JAR not found: {jar_path}")
    return str(jar_path)


def startJVMWithBGP() -> None:
    """Start the JVM with the owlapy-bgp classpath.

    Call this before using any functionality that requires the JVM. If you need
    additional JARs, prefer calling `owlapy.static_funcs.startJVM` directly so you
    can pass the classpath explicitly.
    """
    startJVM(extra_jars=[str(path_to_owlapy_bgp_jar())])
