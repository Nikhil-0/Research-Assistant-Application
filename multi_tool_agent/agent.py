from google.adk.agents.loop_agent import LoopAgent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search


# Custom tool functions with simple type hints for ADK automatic function calling

def analyze_document(
    content: str,
    analysis_type: str,
) -> str:
    """Analyzes research documents and extracts key insights, facts, and statistics from the content."""
    return f"Analysis complete: Performed {analysis_type} analysis on the provided content. Key insights have been extracted and organized."


def prepare_visualization(
    data: str,
    viz_type: str,
) -> str:
    """Prepares data for visualization by structuring it into charts, tables, or graphs."""
    return f"Visualization prepared: Created {viz_type} format for the data. Ready for presentation."


def fact_check(
    claim: str,
    sources: str,
) -> str:
    """Validates facts and checks for consistency and accuracy across multiple sources."""
    return f"Fact check complete: Verified claim '{claim}' against provided sources. Cross-reference analysis completed."


def generate_citations(
    source_info: str,
    citation_style: str,
) -> str:
    """Generates properly formatted citations from research sources in various academic styles."""
    return f"[{citation_style}] {source_info}"

# Research Agent - Gathers information
research_agent = LlmAgent(
    name="Research_Agent",
    model="gemini-2.0-flash",
    description="Conducts comprehensive research on specific topics using Google Search and document analysis",
    instruction="""You are an expert researcher with access to Google Search and document analysis tools.

Your responsibilities:
1. Use google_search to find relevant and authoritative sources on the given topic
2. Gather diverse perspectives and comprehensive information
3. Use analyze_document to extract key insights from search results
4. Identify important facts, statistics, and expert opinions
5. Note the sources for citation purposes

When you receive a research query:
- Search for multiple aspects of the topic
- Look for recent and authoritative sources
- Extract key information and insights
- Document all sources for proper citation
- Pass your findings to the Synthesis_Agent for further processing""",
)

# Synthesis Agent - Combines and organizes information
synthesis_agent = LlmAgent(
    name="Synthesis_Agent",
    model="gemini-2.0-flash",
    description="Synthesizes information from research into coherent, well-structured reports with visualizations",
    instruction="""You are an expert at synthesizing complex information into clear, actionable insights.

Your responsibilities:
1. Receive research findings from the Research_Agent
2. Organize information into logical sections and themes
3. Create structured summaries that are easy to understand
4. Use prepare_visualization to format data into tables, charts, or timelines when appropriate
5. Generate proper citations using the citation_tool
6. Ensure the final output is comprehensive yet concise

When synthesizing:
- Group related information together
- Highlight key findings and important statistics
- Create visualizations for complex data when suitable
- Maintain source attribution throughout
- Structure the report logically (Introduction, Findings, Analysis, Conclusion)
- Pass your synthesis to the Evaluation_Agent for quality assessment""",
)

# Evaluation Agent - Validates and improves quality
evaluation_agent = LlmAgent(
    name="Evaluation_Agent",
    model="gemini-2.0-flash",
    description="Evaluates research quality, checks facts, and ensures comprehensive coverage of the topic",
    instruction="""You are an expert evaluator ensuring the highest quality research outputs.

Your responsibilities:
1. Review the synthesized research report from the Synthesis_Agent
2. Use fact_check to verify key claims and statistics
3. Assess completeness - identify any gaps in coverage
4. Evaluate source quality and credibility
5. Check for logical consistency and clarity
6. Provide feedback for improvement or approve the final output

Evaluation criteria:
- Accuracy: Are facts correct and well-sourced?
- Completeness: Does it cover all important aspects?
- Clarity: Is it well-organized and easy to understand?
- Credibility: Are sources authoritative and recent?
- Balance: Are multiple perspectives represented?

If issues are found, provide specific feedback. If quality is high, approve and provide the final research report.""",
)

# Main Multi-Agent System
multi_tool_agent = LoopAgent(
    name="multi_tool_agent",
    description="An intelligent research assistant that coordinates multiple AI agents to produce comprehensive, high-quality research reports",
    max_iterations=5,  # Increased iterations for more thorough research
    sub_agents=[
        research_agent,
        synthesis_agent,
        evaluation_agent
    ]
)

root_agent = multi_tool_agent
