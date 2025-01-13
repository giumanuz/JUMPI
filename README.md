<p align="center"><h1 align="center">JUMPI</h1></p>
<p align="center">
	<em>This project employs cutting-edge Optical Character Recognition (OCR) and image recognition algorithms to accurately transcribe scanned documents and extract images from them. It offers a robust full-stack solution that includes a user-friendly interface where documents can be uploaded for transcription. Users can edit these transcriptions to ensure accuracy and perform advanced text-based queries within a search-optimized database. This system not only enhances document digitization but also improves the management and retrieval of digital content efficiently.
</CONTEXT></em>
</p>
<p align="center">
<img src="https://img.shields.io/badge/TypeScript-3075C1.svg?style=for-the-badge&logo=TypeScript&logoColor=white" alt="TypeScript" />
<img src="https://img.shields.io/badge/ElasticSearch-E94894.svg?style=for-the-badge&logo=ElasticSearch&logoColor=white" alt="ElasticSearch" />
<img src="https://img.shields.io/badge/OpenAI-FFFFFF.svg?style=for-the-badge&logo=Openai&logoColor=black" alt="OpenAI" />
<img src="https://img.shields.io/badge/Amazon-F89501.svg?style=for-the-badge&logo=AmazonWebServices&logoColor=white" alt="AmazonWebServices" />
<img src="https://img.shields.io/badge/Python-F8C73A.svg?style=for-the-badge&logo=Python&logoColor=black" alt="Python" />
<img src="https://img.shields.io/badge/Docker-3075C1.svg?style=for-the-badge&logo=Docker&logoColor=white" alt="Docker" />
<img src="https://img.shields.io/badge/Flask-A6D189.svg?style=for-the-badge&logo=Flask&logoColor=black" alt="Flask" />
<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=for-the-badge&logo=HTML5&logoColor=white" alt="HTML5" />
<img src="https://img.shields.io/badge/React-00D2F8.svg?style=for-the-badge&logo=React&logoColor=black" alt="React" />
<img src="https://img.shields.io/badge/Azure-ec5125.svg?style=for-the-badge&logo=Azure&logoColor=black" alt="Azure" />
</p>
<br>

##  Table of Contents

- [ Overview](#-overview)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

##  Overview

JUMPI revolutionizes magazine data management by integrating a seamless development environment with Docker, enabling efficient local testing. It features a robust Elasticsearch index for complex queries and a modern React frontend for a consistent user experience. Ideal for publishers seeking efficient content management and retrieval solutions.

---

##  Project Structure

```sh
└── JUMPI/
    ├── docker-compose.yml
    ├── backend
    │   ├── Dockerfile
    │   ├── Dockerfile_dev
    │   ├── app
    │   │   ├── __init__.py
    │   │   ├── config.py
    │   │   ├── routes
    │   │   │   ├── analyze.py
    │   │   │   ├── info.py
    │   │   │   ├── query.py
    │   │   │   ├── upload.py
    │   │   │   └── validate.py
    │   │   ├── services
    │   │   │   ├── database
    │   │   │   │   ├── database.py
    │   │   │   │   ├── elastic.py
    │   │   │   │   └── memory.py
    │   │   │   ├── db_service.py
    │   │   │   ├── file_processor.py
    │   │   │   ├── ocr_readers
    │   │   │   │   ├── aws_reader.py
    │   │   │   │   ├── azure_reader.py
    │   │   │   │   └── ocr_reader.py
    │   │   │   └── openai_client.py
    │   │   └── utils
    │   │       ├── before_request.py
    │   │       ├── classes.py
    │   │       ├── error_handler.py
    │   │       ├── matching_utils.py
    │   │       └── parser.py
    │   ├── aws
    │   │   └── extract_lines.py
    │   ├── azure
    │   │   └── extract_lines.py
    │   ├── commons.py
    │   ├── gpt_prompts
    │   │   ├── is_caption.md
    │   │   ├── single-tool.md
    │   │   └── two-tools.md
    │   ├── main.py
    │   ├── pytest.ini
    │   ├── requirements.txt
    │   └── test
    │       ├── app
    │       │   ├── routes
    │       │   │   ├── test_analyze.py
    │       │   │   ├── test_query.py
    │       │   │   └── test_validate.py
    │       │   ├── services
    │       │   │   ├── database
    │       │   │   │   └── test_elastic.py
    │       │   │   ├── ocr_readers
    │       │   │   │   ├── test_aws_reader.py
    │       │   │   │   └── test_azure_reader.py
    │       │   │   └── test_openai_client.py
    │       │   └── utils
    │       │       ├── test_before_request.py
    │       │       └── test_matching_utils.py
    │       ├── conftest.py
    ├── frontend
    │   ├── eslint.config.js
    │   ├── index.html
    │   ├── package.json
    │   ├── public
    │   │   └── vite.svg
    │   ├── src
    │   │   ├── App.tsx
    │   │   ├── apiKeyUtils.ts
    │   │   ├── axiosInstance.ts
    │   │   ├── components
    │   │   │   ├── ApiKeyInputField.tsx
    │   │   │   ├── ArticleCard.tsx
    │   │   │   ├── InputField.tsx
    │   │   │   ├── MagazineCard.tsx
    │   │   │   └── TextAreaField.tsx
    │   │   ├── main.tsx
    │   │   ├── pages
    │   │   │   ├── AddMagazinePage.tsx
    │   │   │   ├── EditArticlePage.tsx
    │   │   │   ├── EditMagazinePage.tsx
    │   │   │   ├── FormTemplate.tsx
    │   │   │   ├── HomePage.tsx
    │   │   │   ├── MagazineListPage.tsx
    │   │   │   ├── ManageArticlePage.tsx
    │   │   │   ├── QueryResultsPage.tsx
    │   │   │   ├── ResultPage.tsx
    │   │   │   ├── SearchPage.tsx
    │   │   │   └── UploadArticlePage.tsx
    │   │   ├── styles
    │   │   │   ├── FormTemplate.scss
    │   │   │   ├── ResultPage.scss
    │   │   │   └── index.scss
    │   │   ├── types
    │   │   │   ├── api.d.ts
    │   │   │   ├── article.d.ts
    │   │   │   └── magazine.d.ts
    │   │   ├── vite-env.d.ts
    │   │   └── webApi.ts
    │   ├── tsconfig.app.json
    │   ├── tsconfig.json
    │   ├── tsconfig.node.json
    │   └── vite.config.ts

```


###  Project Index
<details open>
	<summary><b><code>JUMPI/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/docker-compose.yml'>docker-compose.yml</a></b></td>
				<td>Facilitate the orchestration of the project's development environment by defining services for both the frontend and backend components<br>Utilize Docker to ensure consistent environments, with the frontend running a Node.js application and the backend executing a Python script<br>Enable seamless communication between services through specified ports and environment variables, supporting efficient local development and testing within the project's architecture.</td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- frontend Submodule -->
		<summary><b>frontend</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/tsconfig.node.json'>tsconfig.node.json</a></b></td>
				<td>Configure TypeScript settings for the frontend's Node.js environment, ensuring compatibility with modern JavaScript features and strict type-checking</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/index.html'>index.html</a></b></td>
				<td>Serves as the entry point for the JUMPI React application, establishing the foundational HTML structure and linking to the main TypeScript module</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/tsconfig.app.json'>tsconfig.app.json</a></b></td>
				<td>The `tsconfig.app.json` file configures TypeScript settings for the frontend of the project, ensuring compatibility with modern JavaScript standards and React</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/package.json'>package.json</a></b></td>
				<td>The frontend/package.json file defines the configuration and dependencies for the frontend component of the project<br>It specifies scripts for development, building, and linting, and includes essential libraries like React, React Router, and Bootstrap</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/vite.config.ts'>vite.config.ts</a></b></td>
				<td>Configures the Vite build tool for the frontend of the project, integrating React support and enabling SCSS preprocessing with specific options</td>
			</tr>
			</table>
			<details>
				<summary><b>src</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/App.tsx'>App.tsx</a></b></td>
						<td>Facilitates the main routing and navigation within the frontend of the application, integrating various pages such as Home, Search, and Magazine management<br>By leveraging React Router, it provides a structured pathway for users to interact with different features.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/main.tsx'>main.tsx</a></b></td>
						<td>Initializes the React application by rendering the main App component into the root element of the HTML document</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/axiosInstance.ts'>axiosInstance.ts</a></b></td>
						<td>Establishes a centralized Axios instance configured with a base URL sourced from environment variables, facilitating consistent API communication across the frontend<br>By standardizing API requests, it enhances maintainability and scalability within the codebase.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/webApi.ts'>webApi.ts</a></b></td>
						<td>Facilitates interaction with the backend API by providing functions to retrieve and manipulate magazine and article data<br>It supports fetching magazine details, retrieving articles by magazine ID, and uploading new articles with associated scans.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/apiKeyUtils.ts'>apiKeyUtils.ts</a></b></td>
						<td>ApiKeyUtils manages API key storage and validation within the frontend architecture<br>It ensures the API key is securely stored in local storage, updates the axios instance with the key for authenticated requests, and provides functionality to validate the key's authenticity</td>
					</tr>
					</table>
					<details>
						<summary><b>types</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/types/magazine.d.ts'>magazine.d.ts</a></b></td>
								<td>Define the structure for magazine-related data within the frontend of the application.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/types/api.d.ts'>api.d.ts</a></b></td>
								<td>Defines TypeScript types for handling API responses related to article uploads and scan results within the frontend.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/types/article.d.ts'>article.d.ts</a></b></td>
								<td>Define the structure and types for articles within the frontend of the project, facilitating consistent data handling and manipulation.</td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>styles</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/styles/index.scss'>index.scss</a></b></td>
								<td>Define the primary color theme for the frontend by customizing Bootstrap's default styles.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/styles/ResultPage.scss'>ResultPage.scss</a></b></td>
								<td>Enhances the visual presentation of the result page by styling text and image containers in the ResultPage.tsx.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/styles/FormTemplate.scss'>FormTemplate.scss</a></b></td>
								<td>Enhances the visual styling of form components within the frontend of the project by defining layout and design elements such as margins, padding, and border radius.</td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>components</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/components/InputField.tsx'>InputField.tsx</a></b></td>
								<td>InputField component provides a reusable and customizable input element for the frontend of the application.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/components/ArticleCard.tsx'>ArticleCard.tsx</a></b></td>
								<td>ArticleCard component enhances the user interface by displaying individual articles with key details such as title, author, and creation date.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/components/ApiKeyInputField.tsx'>ApiKeyInputField.tsx</a></b></td>
								<td>ApiKeyInputField component facilitates user interaction by allowing the input of an API key.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/components/TextAreaField.tsx'>TextAreaField.tsx</a></b></td>
								<td>TextAreaField component enhances the user interface by providing a customizable text area input element within the frontend of the application.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/components/MagazineCard.tsx'>MagazineCard.tsx</a></b></td>
								<td>The MagazineCard component in the frontend of the project serves as a user interface element for displaying magazine details.</td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>pages</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/pages/QueryResultsPage.tsx'>QueryResultsPage.tsx</a></b></td>
								<td>QueryResultPage serves as a user interface component that displays search results within the application<br>It retrieves search results from the navigation state and presents them in a structured format using ArticleCard components<br>If no results are found, it informs the user accordingly.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/pages/MagazineListPage.tsx'>MagazineListPage.tsx</a></b></td>
								<td>Display a list of magazines within the frontend of the application<br>It retrieves magazine data, allows users to expand magazine details, and provides navigation to upload articles, edit magazine details, or manage articles associated with each magazine</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/pages/FormTemplate.tsx'>FormTemplate.tsx</a></b></td>
								<td>Facilitates the creation of form layouts within the frontend architecture by providing a reusable template component.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/pages/EditMagazinePage.tsx'>EditMagazinePage.tsx</a></b></td>
								<td>EditMagazinePage.tsx facilitates the editing of magazine details within the application<br>It retrieves magazine data based on a provided ID, allows users to modify fields such as name, publisher, edition, date, genres, categories, and abstract, and submits the updated information to the server.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/pages/EditArticlePage.tsx'>EditArticlePage.tsx</a></b></td>
								<td>EditArticlePage.tsx facilitates the editing of existing articles within the application<br>It provides a user interface for modifying article details such as title, author, page range, and content<br>Upon submission, it validates the input and sends an update request to the backend<br>Successful updates trigger a navigation back to the homepage, enhancing the user experience by providing immediate feedback on the operation's success.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/pages/ManageArticlePage.tsx'>ManageArticlePage.tsx</a></b></td>
								<td>ManageArticlePage.tsx facilitates the management of articles within a specific magazine by retrieving and displaying articles based on a magazine ID obtained from the URL query parameters<br>It provides an interface for users to view, edit, and navigate through articles associated with a magazine, enhancing the user experience by dynamically loading relevant data and enabling seamless article management within the frontend architecture.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/pages/SearchPage.tsx'>SearchPage.tsx</a></b></td>
								<td>Facilitates user interaction for searching articles within the application by providing a form interface to input search parameters such as magazine details and article specifics<br>Utilizes these inputs to query the backend for matching articles and navigates to a results page upon successful retrieval<br>Enhances user experience by managing loading states and handling errors gracefully during the search process.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/pages/AddMagazinePage.tsx'>AddMagazinePage.tsx</a></b></td>
								<td>Facilitates the addition of new magazines to the system by providing a user interface for inputting magazine details such as name, publisher, edition, categories, genres, date, and abstract<br>It handles form submission, processes input data, and communicates with the backend to store the magazine information<br>Upon successful submission, it navigates users to the article upload page, enhancing the magazine management workflow.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/pages/UploadArticlePage.tsx'>UploadArticlePage.tsx</a></b></td>
								<td>Facilitates the uploading of articles by allowing users to input article details such as title, author, and page range, and upload associated images<br>Validates input data and manages the submission process, including error handling and navigation to a results page upon successful upload<br>Integrates with the web API to process the uploaded article and images, contributing to the frontend's functionality within the overall project architecture.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/pages/ResultPage.tsx'>ResultPage.tsx</a></b></td>
								<td>ResultPage component in the frontend of the project architecture provides a user interface for displaying the results of document analysis<br>It retrieves data from the navigation state, presenting article details, extracted text, and image comparisons<br>If no data is available, it prompts users to return to the upload page, ensuring a seamless user experience in navigating and viewing analysis outcomes.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/frontend/src/pages/HomePage.tsx'>HomePage.tsx</a></b></td>
								<td>Facilitates user interaction with the application by providing a homepage interface where users can input and validate an API key<br>Determines access to the "Search" and "Upload" functionalities based on the validity of the API key.</td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- backend Submodule -->
		<summary><b>backend</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/pytest.ini'>pytest.ini</a></b></td>
				<td>Sets the Python path for Pytest, ensuring tests can find and import modules from the project's root directory<br>This configuration supports efficient test execution and integration across the backend, maintaining code quality<br>It is essential for robust and reliable software development within the project's architecture.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/requirements.txt'>requirements.txt</a></b></td>
				<td>Define the dependencies required for the backend component of the project, ensuring compatibility and functionality across various modules<br>By specifying versions for libraries such as Flask, Elasticsearch, and Azure AI, it facilitates seamless integration with cloud services, enhances API capabilities, and supports testing and code quality<br>This setup is crucial for maintaining a robust and scalable backend architecture within the overall codebase.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/commons.py'>commons.py</a></b></td>
				<td>Extracts and represents text lines from Azure JSON outputs using classes for geometric shapes and text lines.<br>Creates polygons and lines to compare text content across Azure, AWS, and GPT.<br>Essential for text recognition and alignment tasks in the project.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/.env_sample'>.env_sample</a></b></td>
				<td>Defines essential environment variables for backend configuration, enabling integration with services like OpenAI, Elasticsearch, AWS, and Document Intelligence<br>Sets parameters for CORS, debugging, and server hosting, ensuring efficient backend operation<br>Crucial for maintaining secure connections and effective interaction with various APIs and services.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/main.py'>main.py</a></b></td>
				<td>The backend/main.py file initializes and runs the web application by loading environment variables, setting up configuration, and creating the app instance<br>It ensures the application is configured with necessary parameters like the host, port, and API keys<br>This file acts as the entry point for the backend, facilitating the integration of external services and enabling the application to operate in different environments.</td>
			</tr>
			</table>
			<details>
				<summary><b>app</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/config.py'>config.py</a></b></td>
						<td>Configure and manage application settings and temporary directories within the backend architecture<br>The configuration class centralizes key parameters such as API keys and directory paths, ensuring consistent access across the application<br>It also provides methods to create and reset temporary directories, supporting organized data handling and storage.</td>
					</tr>
					</table>
					<details>
						<summary><b>utils</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/utils/before_request.py'>before_request.py</a></b></td>
								<td>Ensure secure API access by implementing a pre-request check for API keys in the backend application<br>The setup function integrates with the Flask app to intercept incoming requests, verifying the presence of an 'X-API-KEY' in the headers<br>If absent, it returns an error response, thereby enforcing authentication and safeguarding the application's endpoints from unauthorized access.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/utils/parser.py'>parser.py</a></b></td>
								<td>Facilitates data transformation between snake_case and camelCase formats, enhancing compatibility and readability across different components of the codebase<br>By providing utility functions for converting both individual strings and dictionary keys, it supports seamless integration and data exchange between systems or modules that adhere to different naming conventions, thereby promoting consistency and reducing potential errors in data handling.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/utils/error_handler.py'>error_handler.py</a></b></td>
								<td>Enhances the application's robustness by managing errors and exceptions, particularly those related to Elasticsearch<br>It logs errors and provides user-friendly error messages, ensuring that unauthorized access and bad requests are appropriately handled.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/utils/classes.py'>classes.py</a></b></td>
								<td>Defines data structures and utility methods for managing articles and magazines within the backend application<br>It provides a framework for creating, querying, and updating instances of articles and magazines, including handling metadata such as creation and modification timestamps<br>The code supports the representation of article content, page scans, and figures, facilitating organized data management and manipulation in the broader project architecture.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/utils/matching_utils.py'>matching_utils.py</a></b></td>
								<td>Facilitates the comparison and alignment of text extracted from Azure and AWS services by leveraging OpenAI's GPT model to enhance matching accuracy<br>It processes files to extract lines, matches them using similarity ratios, and generates visual and textual reports highlighting discrepancies.</td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>routes</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/routes/query.py'>query.py</a></b></td>
								<td>Defines a route for querying magazine and article data<br>Uses query parameters to filter results based on attributes like magazine name, date, publisher, genres, and article details<br>Integrates with the database service to retrieve and return filtered data.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/routes/upload.py'>upload.py</a></b></td>
								<td>Provides endpoints for uploading, retrieving, and updating magazines and articles<br>Handles data conversion between camelCase and snake_case, processes file uploads, and interacts with the database<br>Includes error handling for missing arguments.</td>
							</tr>
							<tr>
								<tr>
									<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/routes/validate.py'>validate.py</a></b></td>
									<td>Validates API key by checking database connection availability. Ensures API key validity only if the database is accessible. Contributes to security and reliability by verifying credentials before allowing operations.</td>
								</tr>
								<tr>
									<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/routes/info.py'>info.py</a></b></td>
									<td>Provides endpoints for retrieving magazine and article information. Handles HTTP GET requests, ensuring required parameters and managing errors. Fetches data from the database, converting it to camel case for client use.</td>
								</tr>
								<tr>
									<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/routes/analyze.py'>analyze.py</a></b></td>
									<td>Processes uploaded files for document analysis, extracting metadata to create and store magazine and article objects. Validates input data, extracts text and images, returns comparisons.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>services</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/services/file_processor.py'>file_processor.py</a></b></td>
								<td>Facilitates the processing of uploaded files by orchestrating OCR operations using AWS and Azure services, extracting text, and generating base64-encoded comparison images<br>It ensures thread-safe execution and manages temporary directories for efficient file handling<br>The processed results, including combined text and page offsets, are returned for further use within the application, supporting document analysis and comparison functionalities.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/services/openai_client.py'>openai_client.py</a></b></td>
								<td>Facilitates interaction with the OpenAI API by providing a client that generates chat completions based on user input<br>It configures parameters such as system prompts, token limits, and temperature settings to tailor responses<br>This component is integral to the backend, enabling dynamic and context-aware conversational capabilities within the broader application architecture.</td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/services/db_service.py'>db_service.py</a></b></td>
								<td>Establishes a connection to an Elasticsearch database by configuring the database instance with the appropriate URL and logging level based on the application's configuration settings<br>Integrates the database instance into the broader application architecture, ensuring that the database service is accessible throughout the backend.</td>
							</tr>
							</table>
							<details>
								<summary><b>database</b></summary>
								<blockquote>
									<table>
									<tr>
										<tr>
											<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/services/database/memory.py'>memory.py</a></b></td>
											<td>Provides in-memory storage for managing magazines and articles. Supports basic operations like adding, retrieving, and searching without persistent storage. Useful for testing and development.</td>
										</tr>
										<tr>
											<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/services/database/database.py'>database.py</a></b></td>
											<td>Defines an abstract base class for database operations. Supports adding, retrieving, updating, and searching for magazines and articles. Ensures consistent data management.</td>
										</tr>
										<tr>
											<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/services/database/elastic.py'>elastic.py</a></b></td>
											<td>Interacts with Elasticsearch to manage and query magazine and article data. Supports adding, retrieving, updating, and searching. Enhances data management and search capabilities.</td>
										</tr>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>ocr_readers</b></summary>
								<blockquote>
									<table>
									<tr>
										<tr>
											<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/services/ocr_readers/ocr_reader.py'>ocr_reader.py</a></b></td>
											<td>Defines an abstract base class for OCR framework for implementing OCR capabilities to extract text lines from images.</td>
										</tr>
										<tr>
											<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/services/ocr_readers/azure_reader.py'>azure_reader.py</a></b></td>
											<td>Integrates Azure's Document Intelligence to analyze and extract text from images, processing documents to identify lines, captions, and figures.</td>
										</tr>
										<tr>
											<td><b><a href='https://github.com/giumanuz/JUMPI/blob/master/backend/app/services/ocr_readers/aws_reader.py'>aws_reader.py</a></b></td>
											<td>Uses AWS Textract to analyze and extract text from images, integrating with the OCR service to retrieve text lines and save results as JSON.</td>
										</tr>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
				</blockquote>
			</details>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with JUMPI, ensure your runtime environment meets the following requirements:

- **Container Runtime:** Docker

###  Installation and Usage

Install JUMPI using one of the following methods:

**Build from source:**

1. Clone the JUMPI repository:
```sh
❯ git clone https://github.com/giumanuz/JUMPI
```

2. Navigate to the project directory:
```sh
❯ cd JUMPI
```

3. Start the app:

**Using `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker compose up -d 
```

---

##  Contributing

- **💬 [Join the Discussions](https://github.com/giumanuz/JUMPI/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/giumanuz/JUMPI/issues)**: Submit bugs found or log feature requests for the `JUMPI` project.
- **💡 [Submit Pull Requests](https://github.com/giumanuz/JUMPI/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/giumanuz/JUMPI
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!