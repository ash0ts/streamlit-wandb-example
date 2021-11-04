# Referenced from: https://github.com/wandb/client/blob/0ea159693996df0f22b408ba38512178bb63104d/wandb/jupyter.py#L55
import wandb
from dotenv import load_dotenv, find_dotenv
import pandas as pd

load_dotenv(find_dotenv())

api = wandb.Api()


class IFrame(object):
    #TODO: Rename

    def __init__(self, path=None, opts=None):
        self.path = path
        self.api = wandb.Api()
        self.opts = opts or {}
        self.displayed = False
        self.height = self.opts.get("height", 420)

    # def maybe_display(self) -> bool:
    #     if not self.displayed and (self.path or wandb.run):
    #         display(self)
    #     return self.displayed

    def to_html(self):
        try:
            self.displayed = True
            if self.opts.get("workspace", False):
                if self.path is None and wandb.run:
                    self.path = wandb.run.path
            if isinstance(self.path, str):
                object = self.api.from_path(self.path)
            else:
                object = wandb.run
            if object is None:
                if wandb.Api().api_key is None:
                    return "You must be logged in to render wandb, run `wandb.login()` or pass environment variables"
                else:
                    object = self.api.project(
                        "/".join(
                            [
                                wandb.Api().default_entity,
                                wandb.util.auto_project_name(None),
                            ]
                        )
                    )
            html_object = object.to_html(self.height, hidden=False)
            jupyterless_html_object = html_object.replace("?jupyter=true", "")
            return jupyterless_html_object
        except wandb.Error as e:
            self.displayed = False
            return "Can't display wandb interface<br/>{}".format(e)


def get_projects(entity, height=720):
    projects = {}
    for project in api.projects(entity):
        projects[project.name] = project.to_html(height=height)
    return projects


def get_runs(entity, project):

    # entity, project = "<entity>", "<project>"  # set to your entity and project
    runs = api.runs(f"{entity}/{project}")

    id_list, state_list, summary_list, config_list, name_list = [], [], [], [], []
    for run in runs:
        id_list.append(run.id)
        state_list.append(run.state)
        # .summary contains the output keys/values for metrics like accuracy.
        #  We call ._json_dict to omit large files
        summary_list.append(run.summary._json_dict)

        # .config contains the hyperparameters.
        #  We remove special values that start with _.
        config_list.append(
            {k: v for k, v in run.config.items()
             if not k.startswith('_')})

        # .name is the human-readable name of the run.
        name_list.append(run.name)

    runs_df = pd.DataFrame({
        "id": id_list,
        "state": state_list,
        "summary": summary_list,
        "config": config_list,
        "name": name_list
    })

    return runs_df
