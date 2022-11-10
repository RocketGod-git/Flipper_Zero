# #!/usr/bin/env python

# TODO: It isn't currently clear how to best embed arbitrary files and load them
# https://flit.readthedocs.io/en/latest/pyproject_toml.html#build-system-section
# https://flit.readthedocs.io/en/latest/index.html
# https://dx13.co.uk/articles/2020/01/02/python-packaging-in-2020/
# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
# https://setuptools.readthedocs.io/en/latest/userguide/datafiles.html
# pip3 install .

# import setuptools
# import codecs
# import os.path
# from pathlib import Path
# import json


# def read(rel_path):
#     here = os.path.abspath(os.path.dirname(__file__))
#     with codecs.open(os.path.join(here, rel_path), "r") as fp:
#         return fp.read()


# def get_version(rel_path):
#     for line in read(rel_path).splitlines():
#         if line.startswith("__version__"):
#             delim = '"' if '"' in line else "'"
#             return line.split(delim)[1]
#     else:
#         raise RuntimeError("Unable to find version string.")


# # TODO: Find a nicer way of bundling dependencies in the future. This is copied from toolbox/server for now.
# def get_relative_custom_server_file_paths():
#     root_path = Path(__file__).parent
#     config_path = root_path / Path("toolbox/config.json")
#     server_files = {}
#     with open(config_path) as config_file:
#         config = json.load(config_file)

#     for config_value in config["server"]:
#         server_path = config_value["server_path"]
#         local_path = config_value["local_path"]
#         if server_path in server_files:
#             raise ValueError(
#                 f"Duplicate server_path '{server_path}' for local_path '{local_path}'"
#             )
#         local_path = root_path / local_path
#         if not local_path.is_file():
#             raise ValueError(f"local_path '{local_path}' is not a valid file.")

#         server_files[server_path] = Path(local_path)

#     relative_file_paths = [str(server_file.relative_to(root_path)) for server_file in server_files.values()]
#     import pdb; pdb.set_trace()
#     return relative_file_paths


# if __name__ == "__main__":
#     setuptools.setup(
#         name="toolbox",
#         description="ctf toolbox",
#         long_description=open("readme.md").read(),
#         url="https://github.com/AlanFoster/toolbox.git",
#         version=get_version("toolbox/__init__.py"),
#         scripts=["bin/toolbox"],
#         packages=["toolbox", "toolbox.server"],
#         install_requires=["click", "flask", "netifaces"],
#         zip_safe=False,
#         package_data={"toolbox.server": ["templates/*"]},
#         include_package_data=True,
#         data_files=[("", get_relative_custom_server_file_paths())],
#     )
