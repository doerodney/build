"""Creates a manifest of the contents of a specified container."""
from argparse import ArgumentParser
from contextlib import redirect_stdout
import subprocess
import tarfile

def create_container(image_id):
    r"""Creates an instance of the specified image, but does not run it. \
    Returns the container id."""
    container_id = ''
    args = ['docker', 'create', image_id]
    result = subprocess.run(args, capture_output=True)
    container_id = result.stdout.decode('utf-8').rstrip()

    return container_id


def export_archive(archive_filename, manifest_filename):
    """Exports a tar file to a text file."""
    tf = tarfile.open(archive_filename)
    with open(manifest_filename, 'w') as f:
        with redirect_stdout(f):
            tf.list(verbose=True)
    tf.close()


def export_container(container_id, filename):
    """Exports a container to a tar file."""
    args = ['docker', 'export', f'--output={filename}', container_id]
    subprocess.run(args)


def generate_image_manifest(repository, tag):
    """Creates a manifest of the specified docker repository and optional tag."""
    repo_str = get_repo_str(repository, tag)

    # Wrapper for:  docker image ls repository:tag
    image_id = get_image_identifier(repository, tag)
    if image_id is not None:
        print(f'Image identifer for {repo_str} is {image_id}.')

        # Wrapper for:  docker create image_id
        container_id = create_container(image_id)
        print(f'Created container {container_id}.')

        # Wrapper for:  docker export --output="<repository>.tar" container_id
        archive_filename = f'{repository}.tar'
        export_container(container_id, archive_filename)
        print(f'Exported container {container_id} to file {archive_filename}.')

        manifest_filename = f'{repository}.manifest.txt'
        # Wrapper for:  tar -tvf <repository>.tar > <repository>.manifest.txt
        export_archive(archive_filename, manifest_filename)
        print(f'Directed view of {archive_filename} content to {manifest_filename}.')

        # Wrapper for: docker rm --force container_id
        remove_container(container_id)
        print(f'Removed container {container_id}.')

    else:
        print(f'No image is available for {repo_str}.')


def get_image_identifier(repository, tag):
    r"""Returns the image identifier of the specified repository, \
    or None if the repository does not exist."""
    image_id = None

    repo_str = get_repo_str(repository, tag)
    args = ['docker', 'image', 'ls', repo_str]

    # Create a subprocess to get the image identifer.
    result = subprocess.run(args, capture_output=True)
    lines = result.stdout.decode('utf-8').split('\n')
    len_data = len(lines[1])
    if len_data > 0:  # More than just a header...
        fields = lines[1].split()
        image_id = fields[2]

    return image_id


def get_repo_str(repository, tag):
    """Creates a string to identify the combination of repository and tag."""
    repo_str = repository
    tag_len = len(tag)
    if tag_len > 0:
        repo_str = f'{repository}:{tag}'

    return repo_str


def remove_container(container_id):
    """Removes an instance of a docker container."""
    args = ['docker', 'rm', '--force', container_id]
    subprocess.run(args, capture_output=True)


def main():
    """Entry point"""
    parser = ArgumentParser()
    parser.add_argument('-r', '--repository', help='docker image repository',
                        dest='repository', required=True)
    parser.add_argument('-t', '--tag', help='docker image tag',
                        dest='tag', required=False, default='')
    args = parser.parse_args()

    generate_image_manifest(args.repository, args.tag)


if __name__ == '__main__':
    main()
