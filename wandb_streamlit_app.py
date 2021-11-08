import streamlit as st
from dotenv import load_dotenv, find_dotenv
from wandb_utils import get_projects, get_runs, get_run_iframe
import streamlit.components.v1 as components
import os

load_dotenv(find_dotenv())

# TODO: Allow user to login and input their API code
# TODO: Add button to make and train a run showing off all useful run stuff (need to unify this for demos)
# TODO: Allow users to see how to use artifacts and then use normal streamlit


def main():
    st.title("Streamlit w/ WANDB")
    menu = ["Embed WANDB", "Use WANDB Artifacts"]
    menu_choice = st.sidebar.selectbox('Menu', menu)
    if menu_choice == 'Embed WANDB':
        st.subheader("WANDB IFrame test")

        # TODO: Create a central demo user? Make a CLI arg?
        # TODO: Read size of available screen in streamlit to use as height/width
        entity = os.environ.get("WANDB_ENTITY", "demo-user")
        height = 720

        # Get list of projects for provided entity whose API key matches
        # Show all those list of projects as selectable options in the sidebar while also grabbing the Iframe link
        # Then display the iframe of the selected project
        projects = get_projects(entity, height=720)
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
    elif menu_choice == "Use WANDB Artifacts":
        st.subheader("#TODO")


        # TODO: Add cli arguments
if __name__ == '__main__':
    main()
