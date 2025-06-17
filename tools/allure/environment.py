from config import settings
import platform
import sys



def create_allure_environment_file():
    os_info = f"{platform.system()}, {platform.release()}"
    python_version = sys.version

    items = [f"{key}={value}" for key, value in settings.model_dump().items()]
    environment_items = [
        f"os_info={os_info}",
        f"python_version={python_version}"
    ]

    all_items = items + environment_items
    properties = "\n".join(all_items)

    with open(settings.allure_results_dir.joinpath("environment.properties"), "w+") as file:
        file.write(properties)

