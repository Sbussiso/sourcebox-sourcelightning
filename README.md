# Sorce Lightning
<br/>

> ### Source Lightning is a service to provide local AI and templates off the SourceBox platform and straight on to your local machine. Wether you are looking for a quick local chat, a usefull agent, or building your own project you can count on Source Lightning getting you started lightning fast!

<br>
<br>

## Chat Applications

### Download chatbots to use locally in your console.
- Choose between models like OpenAI, Mistral, and Gemini
- Access models quickly and locally, no sign in required

### best for quick queries or when you dont feel like logging in!


<br/>

### Download AI powered application to your local machine
- Monitor your machine load and specs with a full AI operations summary using PC scanner.
- Query your local files with our handy File Reader.
- Instantly Generate and automatically set PC backgrounds with nothing but a prompt with our Wallpaper Generator.
- access quickly and locally, no sign in required.


<br/>


## PC Scanner
### The PC Scanner app scans your system specs and resources to give you a simplified system report

### Required
- Internet connection for AI model

<br/>

### GPU
Scans your GPU type and load.

> Scans your GPU type and load, providing detailed information on the current state of your graphics processing unit. This includes the model name, memory usage (both available and used), temperature, and system performance metrics such as the number of physical cores, logical threads, and GPU clock speeds. Additionally, it tracks how much memory is being used by your GPU in real-time, allowing you to monitor its efficiency and temperature during tasks. Keeping an eye on GPU load is crucial for graphic-intensive applications like gaming, 3D modeling, or video rendering. This data helps diagnose potential bottlenecks, overheating issues, or resource constraints.

<br/>

![image](https://github.com/user-attachments/assets/bc9602a5-56c7-48bb-a175-9f41aca5417d)

### CPU
Scans your CPU type and load.

> Scans your CPU type and load, providing real-time insights into your processor’s performance. It includes information such as CPU frequency, the number of physical cores and logical threads, as well as per-core usage statistics. The display also shows load averages over the past 1, 5, and 15 minutes, helping users monitor CPU load over time. Additional system metrics like context switches, interrupts, and system idle time are provided to help you gauge your processor's workload and efficiency. This data is critical for identifying whether your CPU is under heavy load or if there are opportunities to optimize for better performance in multi-core environments.

<br/>

![image](https://github.com/user-attachments/assets/dfca8c2e-2ec5-4e67-85a8-d8eda318ad4d)

### Network
Scans your network load.

<br/>

> Scans your network load and provides detailed statistics about the current state of your network interfaces. This data includes the amount of data sent and received over each interface, as well as the number of packets transmitted and received. It also tracks any errors in transmission and reception, as well as packet drops. Monitoring your network load is essential for identifying bottlenecks, optimizing performance, and troubleshooting connectivity issues. This information can help you diagnose problems such as slow internet connections, packet loss, or network interface failures.

<br/>

![image](https://github.com/user-attachments/assets/b2d63c55-aa58-437a-aa5c-3609240bc0df)

### Memory
Scans your systems memory.

<br/>

> Scans your system’s memory usage and provides a breakdown of available, used, and cached memory. It also shows important details such as the amount of swap space in use, cache memory, and memory allocated for system buffers. This insight is crucial for understanding how your system is handling memory resources, whether it's running efficiently or if it's at risk of running out of memory. Monitoring memory usage helps prevent system slowdowns and ensures optimal performance by identifying when you need to free up memory or increase system resources.

<br/>

![image](https://github.com/user-attachments/assets/6dfb255e-ab08-4d55-bd7a-2671096c974f)

### Disk
Scan your systems disc and disc space.

> Scans your system’s disk and provides detailed information about the available storage, file system type, and disk usage. This includes the total size of each mounted disk, the percentage of used space, and details about the read and write activities on each drive. Monitoring your disk space helps ensure that your system is not running out of storage, which can lead to performance degradation or failure of essential processes. Understanding disk usage can also assist in identifying potential storage bottlenecks or the need for disk cleanup.

<br/>

![image](https://github.com/user-attachments/assets/fd910846-dd2a-4b19-b873-96e85a90fd3d)

### System Summary
Get a full system summar with AI after system analysis.

> Get a comprehensive system summary generated by AI after a detailed analysis of your system’s hardware and performance. The summary provides an overview of critical system information, such as the number of CPU cores, memory usage, GPU performance, and disk capacity. It also highlights real-time metrics like CPU load per core, memory availability, and the amount of data being transferred over network interfaces. This summary helps users understand their system’s current health, potential performance issues, and resource utilization, offering valuable insights for optimizing system performance or troubleshooting problems.

<br/>

![image](https://github.com/user-attachments/assets/65b44c7a-3864-4043-8cbc-aac2002c0aa9)

<br/>


## File Reader

### Use the File Reader app to query your local files with a chatbot connecting your local machine to AI

> The File Reader app allows you to easily interact with and query your local files using a chatbot powered by AI, enabling seamless integration between your local machine and advanced AI models. By leveraging this tool, users can open, read, and analyze a variety of file types directly from their local storage, making it simple to extract information and run queries on documents or data sets.

### Required
- Internet connection for AI model
  > An internet connection is required to access the AI model, as the processing of queries happens through the AI system.

### How it works:

> Simply upload a supported file, and the app will parse and analyze the content using a suitable handler based on the file type. The AI then uses this parsed data to generate responses and insights, allowing for interactive discussions with your files.

<br/>

>  Customers.csv
![image](https://github.com/user-attachments/assets/2cdaa7e6-cb0d-4eda-aaec-78147337bdb2)

<br/>

![image](https://github.com/user-attachments/assets/bc123448-9bac-42f4-bb59-8d72a65c342c)

<br/>

### Supported Files:

<br/>

- **Text Files** (.txt, .py, etc.) – handled by read_plain_text().

<br/>

- **PDF Files** (.pdf) – handled by read_pdf() via PyPDF2.
  
<br/>

- **Word Documents** (.docx) – handled by read_word_doc() via python-docx.
  
<br/>

- **Excel Files** (.xlsx) – handled by read_excel() via openpyxl.

<br/>

- **CSV Files** (.csv) – handled by read_csv() via the csv module.

<br/>

- **JSON Files** (.json) – handled by read_json() via the json module.

<br/>

- **HTML Files** (.html) – handled by read_html() via BeautifulSoup.

<br/>

- **XML Files** (.xml) – handled by read_xml() via xml.etree.ElementTree.

<br/>

- **YAML Files** (.yaml, .yml) – handled by read_yaml() via PyYAML.

<br/>

- **INI Configuration Files** (.ini) – handled by read_ini() via configparser.

<br/>

Perfect for:
- Extracting insights from reports, documents, and datasets.
- Running queries on your local files with an AI assistant.
- Quickly accessing relevant information without manually combing through files.




## Wallpaper Generator
### Automatically generate and set AI images as your computer background with nothing but a prompt.

> Transform your desktop effortlessly by generating stunning AI-driven images to use as your wallpaper with just a simple prompt. The Wallpaper Generator combines cutting-edge AI technology with seamless automation to bring your imagination to life and set it as your computer background instantly.

### Required
- Internet connection for AI model
  > An internet connection is needed to access the AI model for image generation.

<br/>

### Image Generation
> Wallpaper Generator uses OpenAI DALLE for the image generation

### How it Works:

> Using OpenAI's powerful DALLE model, the Wallpaper Generator interprets your prompt and creates a high-quality image specifically tailored to be used as your desktop background. From landscapes to abstract art, the possibilities are endless.


<br/>

### Setting your wallpaper

> No need to manually set the generated images yourself. The Wallpaper Generator handles the entire process from creation to application, automatically updating your background with the newly created image, saving you time and effort. Whether you’re looking for a serene nature scene, futuristic cityscapes, or personalized artwork, simply enter your desired prompt, and the Wallpaper Generator will handle the rest. It’s never been easier to refresh your workspace with unique, AI-generated art!

<br/>

![image](https://github.com/user-attachments/assets/c498ee9b-d2f6-4cbb-9ce5-26e101763db3)


<br/>

![image](https://github.com/user-attachments/assets/d0ebe9f1-db9e-4128-8505-39ba4e184763)






<br/>
<br/>
<br/>
<br/>







## Agents

### Download and execute AI agents built for various tasks localy in your console.

> AI Agents are specialized programs that can be downloaded and executed locally on your machine to perform a variety of tasks through the command line. These agents are designed to automate specific workflows and interact with your local environment, allowing you to complete tasks efficiently without the need for internet access once the agent is installed.

### Some features of agents include
> ***Task Automation:*** AI Agents can be prompted to complete a wide range of tasks, from simple operations like opening a console window to more complex file system management or script execution.

<br/>

> ***Local Execution:*** All tasks are performed locally on your system, ensuring faster response times and allowing for offline usage after the initial setup.

<br/>

> ***Prompt-Based Commands:*** Users interact with agents using natural language prompts. For instance, typing a prompt like "Open my console" will instruct the agent to open the command line interface.

<br/>

> ***Versatile Use Cases:*** AI Agents can be configured for various purposes, such as managing files, automating processes, or gathering system information.

<br/>
<br/>

### AI Meets your console with your Local Command Agent.

Take AI to the next step by connecting AI to your local command line!

> Elevate your workflow by integrating AI directly into your local command line with the Local Command Agent. This powerful tool brings AI capabilities to your console, enabling you to execute tasks, run commands, and interact with your system in entirely new ways. From automating repetitive tasks to providing real-time insights, the Local Command Agent seamlessly connects AI to your console, unlocking a new level of productivity and efficiency. Whether you're managing files, running scripts, or querying data, this integration allows you to leverage AI's potential right from your terminal, transforming how you interact with your computer.

<br/>

### Example:

>  "Open my console."
![image](https://github.com/user-attachments/assets/197de441-fbc2-4315-ae95-402e6562fe0c)
![image](https://github.com/user-attachments/assets/a95783ed-82f0-4d3b-b842-e5df625dc54b)

<br/>
<br/>
<br/>
<br/>

### Stay up to date with financial news and get predictions with Finance Agent.

Easily get caught up and stay in the financial know.

<br/>

> ***Market Overview:*** Ask for a summary of how the stock market performed during the day, with key highlights of trends or major events.

<br/>

> ***Stock Predictions:*** Get predictions on where a particular stock might be headed based on recent performance, global events, and market sentiment.

<br/>

> ***Event Impact Analysis:*** Understand how a major event (such as earnings reports or geopolitical news) could affect stock prices and financial markets.

<br/>

### Get more knowlegabe help with your coding projects with Code Agent.

an agent with a code interpreter and stack exchange knowlege

<br/>

> The Code Agent is a powerful AI tool designed to assist with coding projects by offering real-time code interpretation and troubleshooting support. Equipped with a built-in code interpreter and extensive knowledge from Stack Exchange, this agent can help developers of all skill levels improve their code, debug issues, and explore best practices.

### Features:
> ***Code Interpretation:*** The Code Agent can evaluate and execute code snippets, allowing you to test, debug, and refine your programs within your local environment. Whether you're writing Python, JavaScript, or other languages, the Code Agent helps by analyzing your code for errors and offering real-time solutions.

<br/>

> ***Stack Exchange Integration:*** Leveraging the vast knowledge base of Stack Exchange, the agent can provide solutions to common coding problems, answer questions about programming concepts, and suggest optimal coding patterns. This ensures you have access to a wealth of community-driven knowledge without needing to leave your environment.

<br/>

> ***Language Support:*** The Code Agent supports a wide range of programming languages and can assist with syntax clarification, function explanations, and even performance optimization tips based on the language you're using.

<br/>

> ***Error Debugging:*** Easily diagnose issues in your code with detailed explanations of error messages, suggestions for fixes, and links to relevant resources. This allows you to quickly resolve bugs and keep your project on track.

<br/>

(console image 1) (console image 2)

<br/>
<br/>
<br/>
<br/>

### Access and query your Google Resources with Google Agent.

Run an agent connected to your google accounts

<br>

> The Google Agent allows seamless integration with your Google account, providing access to key resources like Gmail, Google Drive, Google Sheets, Google Docs, and more. By connecting directly to your Google services, this agent enables you to manage, query, and automate tasks across your Google ecosystem—all through simple prompts.

<br/>

### Features

<br>

> Gmail Integration: Query your email for specific messages, organize your inbox, or even send emails directly through the agent. Use prompts to find unread emails, search for messages based on keywords, or create drafts.

<br/>

> Google Drive Access: Navigate and manage your Google Drive by searching for files, organizing folders, or retrieving document details. The agent can also help you upload or download files, allowing you to manage your cloud storage with ease.

<br/>

> Google Sheets Queries: Work with spreadsheets by querying and updating your Google Sheets. Whether you need to retrieve specific data, perform calculations, or update cells, the agent helps automate your workflow.

<br/>

> Google Docs Automation: Access and manipulate documents in Google Docs. Create new documents, search for keywords within documents, or make updates to existing content without needing to open Docs manually.

<br/>

> Calendar Management: Query and update your Google Calendar by adding events, checking upcoming appointments, or receiving reminders. The agent simplifies calendar management by syncing directly with your schedule.

<br/>

(console image 1) (console image 2)

<br/>
<br/>
<br/>
<br/>

## Getting Into It With Apps

### PC Scanner

<br/>

> The PC Scanner app scans your system specs and resources to give you a simplified system report

<br/>

### Getting started
> First go to https://sourcebox-sourcelightning-8952e6a21707.herokuapp.com

<br/>

> Next, select either "Apps" or "Agents" using the side arrows and click "Show Downloads".

<br/>

> Select your application based on the descriptions and your requirements.

<br/>

> Click "Download", wait a few seconds, and save it to your machine.

<br/>

> Unzip the files.

<br/>

> If you do not know how to unzip files search here:
<br/>
  [https://www.google.com/search?q=how+to+unzip+a+file&oq=how+to+unzip+a+file&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBCDU3ODhqMGo3qAIIsAIB&sourceid=chrome&ie=UTF-8]




## Getting into it with Agents
instructions for agents

