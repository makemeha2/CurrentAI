from agents.collector import RSSCollectorAgent
from agents.organizer import NewsOrganizerAgent
from agents.reporter import ReportGeneratorAgent
from agents.summarizer import NewsSummarizerAgent
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from state import NewsState


def create_news_workflow(llm: ChatOpenAI = None) -> StateGraph:
    collector = RSSCollectorAgent()
    summarizer = NewsSummarizerAgent(llm)
    organizer = NewsOrganizerAgent(llm)
    reporter = ReportGeneratorAgent()

    workflow = StateGraph(NewsState)
    workflow.add_node("collect", collector.collect_rss)
    workflow.add_node("summarize", summarizer.summarize_news)
    workflow.add_node("organizer", organizer.organize_news)
    workflow.add_node("reporter", reporter.generate_report)

    workflow.set_entry_point("collect") 
    workflow.add_edge("collect", "summarize")
    workflow.add_edge("summarize", "organizer")
    workflow.add_edge("organizer", "reporter")
    workflow.add_edge("reporter", END)

    return workflow.compile() # type: ignore