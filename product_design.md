The Problem: The Signal-to-Noise Ratio University students at large institutions (like KCL) are drowning in information but starving for insight. They face a spectrum of demands: from the logistical ("Where is my timetable?") to the strategic ("How do I maximize my tuition fees via opportunities?").
The Status Quo: High Friction Currently, navigating this requires a disjointed, high-friction workflow: relying on hearsay from seniors, digging through outdated intranets, or scrolling through hundreds of emails. This leads to missed deadlines, anxiety, and an under-utilized university experience.
The Solution: The Intelligent Student Hub We are using AI to build a dynamic information bridge that connects students to the university's ecosystem. Unlike a static website, this tool aggregates, verifies, and personalizes information. It filters the noise to ensure students not only find their classes but discover the high-value opportunities that define their academic and professional future.

# MVP design:
The MVP will simply be a GPT similar AI chat interface, it is free to use, and student can ask any questions about kcl, but to access private content such as email box, student is required to log into their KCL microsoft account via th button in the top right corner

TO solve this problem, the AI requires a through access to updated information, meaning it needs access to:
Website research, and a familiar landscape to all of the KCL website navigation
timetable



# Technical PRD
Core design, we are looking to builds agents that are capable of utilzing different tools to access information public/private mentioned above

The cloud host will be Supabase (credentials in .env)

The front end will use streamlit

We will use langraph for agent workflow: the agent will consist tools such as web browsing, time table access etc

We will call LLM from OpenRouter (credentials in .env)

For the search tool we will use SerpAPI (credentials in .env)

For website crawling we will use Firecrawl (credentials in .env)

For the KCL timetable we will use the iCal subscription
