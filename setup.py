import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="imfilters", # Nome do Pacote
    version="1.0.1",
    author="Wellington Gadelha",
    author_email="contato.informeai@gmail.com",
    description="Pacote para tratamento e aplicação de filtros em imagens.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['Pillow','opencv-python'],
    url="https://github.com/informeai/imfilters",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

