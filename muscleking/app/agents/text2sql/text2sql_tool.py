"""
Text2SQL tool wrapper for the multi-tool workflow.

This node bridges the planner/tool-selection workflow with the
Text2SQL LangGraph pipeline implemented under ``gustobot.application.agents.text2sql``.
"""

from typing import Dict, Any, Coroutine, Callable, List
from muscleking.app.persistence.core.neo4jconn import get_neo4j_graph

from loguru import logger

logger = logger.bind(service="text2sql")

def create_text2sql_tool_node(
        neo4j_graph=None,
) -> Callable[[Dict[str, Any]], Coroutine[Any, Any, Dict[str, Any]]]:
    """
    Create a LangGraph node that executes the Text2SQL workflow.

    Parameters
    ----------
    neo4j_graph : Neo4jGraph | None
        Existing Neo4j graph connection used for schema retrieval. If ``None``,
        the node will attempt to obtain one via ``get_neo4j_graph``.
    """

    async def text2sql_query(state: Dict[str, Any]) -> Dict[str, Any]:
        question = state.get("task") or state.get("question") or ""
        tool_args: Dict[str, Any] = state.get("query_parameters",{}) or {}

        connection_id = tool_args.get("connection_id")
        db_type = tool_args.get("db_type") or "MySQL"
        max_rows = int(tool_args.get("max_rows") or 1000)
        connection_string = tool_args.get("connection_string")
        max_retries = int(tool_args.get("max_retries") or 3)

        errors:List[str] = []

        graph = neo4j_graph
        if graph is None and get_neo4j_graph is not None:
            try:
                graph = get_neo4j_graph()
                logger.info("Obtained Neo4j graph connection for Text2SQL tool.")
            except Exception as e:
                logger.error("Failed to obtain Neo4j graph connection: %s", e)
                errors.append(f"无法连接图数据库: {e}")
                graph = None
        
        #neo4j链接失败兜底机制

        #若LLMAPI无效，兜底机制

        #大模型初始化

        #workflow搭建
        workflow = create_text2sql_workflow(
            llm=text2sql_llm,
            neo4j_graph=graph,
            db_type=db_type,
            connection_string=connection_string,
            max_retries=max_retries,
        )

        #input_state定义

        #workflow执行

        #查询结果映射与payload(负载)构造
        return {
            "cyphers": [
                CypherQueryOutputState(
                    **{
                        "task": question,
                        "query": sql_statement,
                        "errors": errors,
                        "records": records_payload,
                        "steps": ["execute_text2sql_query"],
                    }
                )
            ],
            "steps": ["execute_text2sql_query"],
        }
    
    return text2sql_query