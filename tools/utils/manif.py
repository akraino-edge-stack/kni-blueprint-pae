import os
import sys
import yaml

def get_gvkn(manifest, recurse_lists=False):
    """ Returns a GVKN string for a given manifest object
        GVKN stands for the (Group, Version, Kind, Name)-tuple that uniquely
        identifies a K8s resource in a given namespace. This method returns
        this as string in format "G/V/K|N" such that it can be used as key to
        look up resources. If a manifest doesn't contain any given value,
        use "~G" (resp. ~V, ~K, ~N) instead (like "kustomize" does it). """
    gv = manifest.get("apiVersion", "~G/~V")
    k  = manifest.get("kind", "~K")
    n  = manifest.get("metadata", {}).get("name", "~N")
    if "/" not in gv:
        gv = "~G/" + gv
    gvkn = "{0}/{1}|{2}".format(gv, k, n)

    if gvkn == "~G/v1/List|~N" and recurse_lists:
        gvkns = []
        for item in manifest.get("items", []):
            gvkns.append(get_gvkn(item, recurse_lists))
        return gvkns
    return gvkn

def get_filename(manifest):
    gv = manifest.get("apiVersion", "")
    g  = gv.partition('/')[0]
    k  = manifest.get("kind", "")
    n  = manifest.get("metadata", {}).get("name", "")
    filename = "{0}_{1}_{2}.yaml".format(g, k, n)
    return filename.replace('.', '-').lower()

def read_all_docs(fd):
    """ Reads a multi-doc YAML doc and returns docs as list of multi-line strings. """
    manifests = []
    manifest = ""
    for line in fd:
        if line.strip() == "---" and manifest != "":
            manifests.append(manifest)
            manifest = ""
            continue
        if line.strip() == "":
            continue
        manifest = manifest + line
    manifests.append(manifest)
    return manifests

def read_obj(fd):
    """ Reads a single YAML doc and returns it as YAML object. """
    try:
        manifest = yaml.safe_load(fd)
    except yaml.YAMLError as e:
        sys.exit("Error parsing {0}: {1}".format(fd, e))
    return manifest

def read_all_objs(fd):
    """ Reads a multi-doc YAML doc and returns a list YAML objects. """
    try:
        manifests = yaml.safe_load_all(fd)
    except yaml.YAMLError as e:
        sys.exit("Error parsing {0}: {1}".format(fd, e))
    return manifests

def load(filepath):
    """ Loads a manifest object from file. """
    with open(filepath, 'r') as fd:
        return read_obj(fd)

def load_all(filepath):
    """ Loads a list of manifest objects from a multi-doc file. """
    with open(filepath, 'r') as fd:
        return read_all_objs(fd)

def exist_and_equal(fileA, fileB):
    if not os.path.exists(fileA) or not os.path.exists(fileB):
        return False
    yamlA = load(fileA)
    yamlB = load(fileB)
    return yamlA == yamlB
