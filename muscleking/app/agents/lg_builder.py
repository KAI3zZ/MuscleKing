"""
langgraph 多路由图构造
"""
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from loguru import logger
from muscleking.app.models.model_agents import AdditionalGuardrailsOutput

logger = logger.bind(service="lg_builder")
