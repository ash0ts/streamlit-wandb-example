import streamlit as st
from dotenv import load_dotenv, find_dotenv
from wandb_utils import get_projects, get_runs, get_run_iframe, log_example_html_to_wandb, get_wandb_demo_artifact
import streamlit.components.v1 as components
import os
from pathlib import Path
import json

load_dotenv(find_dotenv())

# TODO: Allow user to login and input their API code
# TODO: Add button to make and train a run showing off all useful run stuff (need to unify this for demos)
# TODO: Allow users to see how to use artifacts and then use normal streamlit


def main():
    st.title("Streamlit w/ WANDB")
    menu = ["Embed WANDB", "Use WANDB Logging"]
    menu_choice = st.sidebar.selectbox('Menu', menu)

    # TODO: Create a central demo user? Make a CLI arg?
    # TODO: Read size of available screen in streamlit to use as height/width
    entity = os.environ.get("WANDB_ENTITY", "demo-user")
    height = 720

    projects = get_projects(entity, height=720)

    if menu_choice == 'Embed WANDB':
        st.subheader("WANDB IFrame test")

        # Get list of projects for provided entity whose API key matches
        # Show all those list of projects as selectable options in the sidebar while also grabbing the Iframe link
        # Then display the iframe of the selected project
        selected_project = st.sidebar.selectbox(
            "Project Name", list(projects.keys()))
        selected_project_iframe = projects[selected_project]
        st.subheader("PROJECT DETAILS:")
        components.html(selected_project_iframe, height=height)

        # For the selected project we grab all the run details available
        # We filter on the state to only display the finished runs
        # Then we populate a selectable list on the sidebar for users to selecte to display the iframe for the run
        runs_details = get_runs(entity, selected_project)
        finished_runs_details = runs_details[runs_details["state"] == "finished"]
        run_ids = finished_runs_details["id"].to_list()
        id_choice = st.sidebar.selectbox("Run ID", run_ids)

        # We load the run from the api and then display it
        selected_run_path = f"{entity}/{selected_project}/{id_choice}"
        run_iframe = get_run_iframe(selected_run_path)
        st.subheader("RUN DETAILS:")
        components.html(run_iframe, height=height)
    elif menu_choice == "Use WANDB Logging":
        st.subheader("Logged HTML IFrame test")

        # Add a button which will run a test run to render for this demo
        if st.button("Run Example"):
            log_example_html_to_wandb()

        selected_project = "Log-Example-HTML"
        if selected_project in projects:
            selected_artifact = "demo_artifacts"
            selected_html_file_name = "demo_html"

            # We load the run from the api and then gather the artifacts to display
            selected_project_path = f"{entity}/{selected_project}"

            # We download all the artifacts to access for the demo
            demo_artifact_path = get_wandb_demo_artifact(
                selected_project_path)

            # A couple of steps are needed to properly load reload the html in via WANDB
            # Use metadata file to find path to the actual html
            # this value is in the `path` key
            demo_html_meta_path = Path(
                demo_artifact_path, f"{selected_html_file_name}.html-file.json")
            with open(demo_html_meta_path, "rb") as f:
                demo_html_meta = json.load(f)

            # Read the contents of the html file into a string to be rendered by streamlit
            demo_html_path = Path(demo_artifact_path, demo_html_meta["path"])
            demo_html = open(demo_html_path, "r")
            demo_html_contents = demo_html.read()

            components.html(demo_html_contents, height=height)

            # demo_html.close()


# TODO: Add cli arguments
if __name__ == '__main__':
    main()
