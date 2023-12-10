import re
import urllib
import pathlib
import hydra
import yaml

_FILE_URI_REGEX = re.compile(r"^file://.+")


def _is_file_uri(uri):
    """Returns True if the passed-in URI is a file:// URI."""
    return _FILE_URI_REGEX.match(uri)

def _parse_file_uri(uri: str) -> str:
    """Converts file URIs to filesystem paths"""
    if _is_file_uri(uri):
        parsed_file_uri = urllib.parse.urlparse(uri)
        return str(
            pathlib.Path(parsed_file_uri.netloc, parsed_file_uri.path, parsed_file_uri.fragment)
        )
    return uri

def _is_local_uri(uri: str) -> bool:
    """Returns True if passed-in URI should be interpreted as a folder on the local filesystem."""
    resolved_uri = pathlib.Path(_parse_file_uri(uri)).resolve()
    print(f"resolved uri: %s" % resolved_uri)
    return resolved_uri.exists()

if __name__ == '__main__':
    with open("config.yaml", "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        print("Load configuration successfully")
    
    remote_path = f"{config['main']['components_repository']}/get_data"
    print(f"remote path: {remote_path}")
    is_uri = _is_file_uri(remote_path)
    print(f"Is it URI file?: {is_uri}" )
    parsed_file_uri = _parse_file_uri(remote_path)
    print(f"parsed_file_uri: {parsed_file_uri}")
    _is_local_uri(remote_path)
    