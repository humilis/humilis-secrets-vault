"""Setuptools entry point."""

import os
import codecs
from setuptools import setup, find_packages

import humilis_secrets_vault.metadata as metadata

dirname = os.path.dirname(__file__)

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, RuntimeError):
    if os.path.isfile("README.md"):
        long_description = codecs.open(os.path.join(dirname, "README.md"),
                                       encoding="utf-8").read()
    else:
        long_description = metadata.description

setup(
    name="humilis-secrets-vault",
    version=metadata.version,
    author=metadata.authors_string,
    author_email=metadata.emails[0],
    include_package_data=True,
    package_data={
        "": ["*.j2", "*.yaml"]},
    packages=find_packages(include=["humilis_secrets_vault"]),
    url=metadata.url,
    license=metadata.license,
    description=metadata.description,
    long_description=long_description,
    install_requires=[
        "humilis>=0.3.0"],
    classifiers=[
        "Programming Language :: Python :: 3"],
    zip_safe=False,
    entry_points={
        "humilis.layers": [
            "secrets-vault=humilis_secrets_vault.__init__:get_layer_path"]}
)
