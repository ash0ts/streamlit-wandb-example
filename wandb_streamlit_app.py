import streamlit as st
from dotenv import load_dotenv, find_dotenv
from wandb_utils import IFrame as wandb_IFrame, get_projects, get_runs
import streamlit.components.v1 as components
import os

load_dotenv(find_dotenv())


def main():
    st.title("Streamlit w/ WANDB")
    menu = ["Embed WANDB", "Use WANDB Artifacts"]
    menu_choice = st.sidebar.selectbox('Menu', menu)
    if menu_choice == 'Embed WANDB':
        st.subheader("WANDB IFrame test")

        # TODO: Create a central demo user? Make a CLI arg?
        entity = os.environ.get("WANDB_ENTITY", "demo-user")
        height = 720

        projects = get_projects(entity, height=720)
        selected_project = st.sidebar.selectbox(
            "Project Name", list(projects.keys()))
        selected_project_iframe = projects[selected_project]
        st.subheader("PROJECT DETAILS:")
        components.html(selected_project_iframe, height=height)

        # selected_project = "uncategorized"

        runs_details = get_runs(entity, selected_project)
        finished_runs_details = runs_details[runs_details["state"] == "finished"]
        run_ids = finished_runs_details["id"].to_list()
        id_choice = st.sidebar.selectbox("Run ID", run_ids)
        # selected_run = api.run(f"{entity}/{project}/{id_choice}")
        selected_run = f"{entity}/{selected_project}/{id_choice}"
        run_iframe = wandb_IFrame(selected_run, {"height": height})
        run_iframe_html = run_iframe.to_html()
        # print(run_iframe_html)
        st.subheader("RUN DETAILS:")
        components.html(run_iframe_html, height=height)
    elif menu_choice == "Use WANDB Artifacts":
        st.subheader("#TODO")

        # TODO: Add cli arguments
if __name__ == '__main__':
    main()
