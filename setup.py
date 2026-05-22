from setuptools import setup, find_packages

setup(
    name="networking",
    version="2.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "networking=networking:main",
        ]
    },
    install_requires=[
        "scapy>=2.5.0",
        "psutil>=5.9.0", 
        "colorama>=0.4.6",
        "tabulate>=0.9.0"
    ],
    author="Falconmx1",
    author_email="tu@email.com",
    description="Herramienta profesional de seguridad en red: escaneo multithreading, detección ARP spoofing, modo sigiloso y reportes HTML",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
    ],
    python_requires=">=3.7",
)
