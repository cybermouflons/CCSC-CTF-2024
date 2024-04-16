import os
import yaml
import sys
from jinja2 import Environment, FileSystemLoader
from urllib.parse import urljoin


class IgnoreSpecificConstructorLoader(yaml.SafeLoader):
    def ignore_constructor(self, node):
        return None


IgnoreSpecificConstructorLoader.add_constructor(
    "!filecontents", IgnoreSpecificConstructorLoader.ignore_constructor
)


def parse_challenge(directory):
    path = os.path.join(directory, "challenge.yml")
    print(path)
    with open(path, "r") as file:
        return yaml.load(file, Loader=IgnoreSpecificConstructorLoader)


def main():
    directories = sys.argv[1].split(" ")
    challenge_categories = {}

    file_loader = FileSystemLoader("/")
    env = Environment(loader=file_loader)
    challenge_readme_tmpl = env.get_template("challenge_README.jinja")

    for directory in directories:
        challenge = parse_challenge(directory)
        category = challenge["category"]
        challenge["dir"] = directory
        challenge["docker_compose_url"] = urljoin("https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/", f"{directory}/docker-compose.yml")
        if category not in challenge_categories:
            challenge_categories[category] = []
        challenge_categories[category].append(challenge)

        chall_readme = challenge_readme_tmpl.render(challenge=challenge)
        with open(os.path.join(directory, "README.md"), "w") as f:
            f.write(chall_readme)

    readme_tmpl = env.get_template("README.jinja")
    output = readme_tmpl.render(challenge_categories=challenge_categories)

    with open("README.md", "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()
