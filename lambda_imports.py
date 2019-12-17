import sys

def manage_imports(config):
    """
    This is needed for finding where the python dependencies the service get installed.
    There are several approaches, this addresses two of them.
    First, if the service is using lambda layers, the contents of the layer zip file
    gets extracted to /opt. In the case of the default serverless-python-requirements
    'layer: true" setting, the default is /opt/python.
    Second method is the serverless-python-requirements zip file method that calls
    'unzip_requirements', which unzips the requirements directory to /tmp/sls-py-req.

    No matter which method is used, it needs to have its path added to sys.path
    before /var/runtime. That directory has very old, out of date versions of very
    commonly used packages (like boto and requests) which can cause confusion and
    frustration if they get loaded instead of the versions deployed with the service.

    :param config: Config dict defined in wsgi_handler.py
    :return:
    """
    if config.get('use_layers', False):
        layer_path = config.get('layer_path', '/opt/python')
        sys.path.insert(1, layer_path)

    else:
        """ This is needed to add the python dependencies serverless-python-requirements
            zip up and unzips into /tmp/sls-py-req
        """
        try:
            import unzip_requirements
        except ImportError:
            pass
