'''
  ******************************************************************************************
      Assembly:                Name
      Filename:                name.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="upload.py" company="Terry D. Eppler">

	     upload.py
	     Copyright ©  2022  Terry Eppler

     Permission is hereby granted, free of charge, to any person obtaining a copy
     of this software and associated documentation files (the “Software”),
     to deal in the Software without restriction,
     including without limitation the rights to use,
     copy, modify, merge, publish, distribute, sublicense,
     and/or sell copies of the Software,
     and to permit persons to whom the Software is furnished to do so,
     subject to the following conditions:

     The above copyright notice and this permission notice shall be included in all
     copies or substantial portions of the Software.

     THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
     INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.
     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
     DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
     ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
     DEALINGS IN THE SOFTWARE.

     You can contact me at:  terryeppler@gmail.com or eppler.terry@epa.gov

  </copyright>
  <summary>
    name.py
  </summary>
  ******************************************************************************************
'''
import streamlit as st
import config as cfg
import openai

with st.sidebar:
	openai_api_key = cfg.OPENAI_API_KEY
	('[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A'
	 '.py)')
	('[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)]('
	 'https://codespaces.new/streamlit/llm-examples?quickstart=1)')

st.title( '📝 Document Query' )
uploaded_file = st.file_uploader( 'Upload a document', type=('txt', 'md') )
question = st.text_input( 'Ask something about the article',
	placeholder='Can you give me a short summary?', disabled=not uploaded_file, )

if uploaded_file and question and not openai_api_key:
	st.info( 'Please add your OpenAI API key to continue.' )

if uploaded_file and question and openai_api_key:
	article = uploaded_file.read( ).decode( )
	prompt = f""" Here's an article:\n\n<article>
    {article}\n\n</article>\n\n{question} """
	
	client = openai.Client( api_key=openai_api_key )
	response = client.completions.create( prompt=prompt, model='gpt-5-nano',
		max_tokens_to_sample=10000, )
	st.write( '### Answer' )
	st.write( response.completion )
