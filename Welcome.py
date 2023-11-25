# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Patient Dashboard",
        page_icon="👋",
    )

    st.write("# Welcome to your Patient Dashboard! 👋")

    st.sidebar.success("Select a patient view above.")

    st.markdown(
        """
This is a demo of the patient monitoring dashboard that would be used to remotely monitor patients with or at risk of hypertensive disorders of pregnancy in Zimbabwe    """
    )

if __name__ == "__main__":
    run()
