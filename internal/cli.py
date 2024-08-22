import os
import click

@click.command()
@click.argument('project_name')
def create_project(project_name):
    """Create a new FastAPI project with the specified name."""
    # Define the directory structure
    directories = [
        project_name,
        os.path.join(project_name, 'tests'),
    ]

    # Define the files to create
    files = [
        os.path.join(project_name, '__init__.py'),
        os.path.join(project_name, 'models.py'),
        os.path.join(project_name, 'resources.py'),
        os.path.join(project_name, 'schemas.py'),
        os.path.join(project_name, 'tests', '__init__.py'),
    ]

    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        click.echo(f'Created directory: {directory}')

    # Create files
    for file in files:
        with open(file, 'w') as f:
            # Add initial content to specific files if needed
            if file.endswith('urls.py'):
                f.write('from fastapi import APIRouter\n\nrouter = APIRouter()\n\n# Add your routes here\n')
            pass  # Create an empty file
        click.echo(f'Created file: {file}')

if __name__ == '__main__':
    create_project()
