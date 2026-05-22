from setuptools import setup, find_packages

setup(
    name="networking",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "networking=networking:main",
        ]
    },
    install_requires=[
        # No agregamos scapy para mantenerlo ligero
        # Para Windows con --ids se necesitaría pypcap o npcap
    ],
    author="Falconmx1",
    description="Herramienta de seguridad en red: detección de intrusos + escaneo de puertos",
    license="MIT",
)
