from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData


def process_agent_data(agent_data: AgentData) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
    agent_data (AgentData): Agent data that contains accelerometer, GPS, and timestamp.
    Returns:
    processed_data (ProcessedAgentData): Processed data containing the classified state of
    the road surface and agent data.
    """
    if abs(agent_data.accelerometer.y) > 2000:
        road_state = "bumpy"
    elif abs(agent_data.accelerometer.y) > 1000:
        road_state = "rough"
    elif abs(agent_data.accelerometer.y) > 500:
        road_state = "normal"
    elif abs(agent_data.accelerometer.y) > 100:
        road_state = "smooth"
    elif abs(agent_data.accelerometer.y) > 50:
        road_state = "very smooth"
    else:
        road_state = "ideal"

    return ProcessedAgentData(road_state=road_state, agent_data=agent_data)
