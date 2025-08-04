# IBM watsonx Orchestrate Flow Builder Demonstration (Local AI Agents) [Reference](https://www.youtube.com/watch?v=kv0PIsVWtmA)

## Project Overview

This project provides a practical demonstration of the **new Flow Builder functionality within IBM watsonx Orchestrate Developer Edition**, focusing on its use with local AI agents [1]. The primary objective is to showcase **how to visualise, debug, and deploy tool flows** directly within the watsonx Orchestrate environment [1].

The video upon which this README is based illustrates a simple implementation to highlight the Flow Builder's capabilities, rather than complex agent use cases or advanced prompting techniques [1].

## Key Features & Concepts Demonstrated

*   **New Flow Builder Functionality**: This is a recently introduced feature in watsonx Orchestrate, allowing for graphical construction of tool flows [1].
*   **Flows as Tools**: Within watsonx Orchestrate, the flows you build using the Flow Builder are treated and accessed as tools that agents can utilise [1].
*   **Local AI Agents Integration**: The demonstration specifically uses watsonx Orchestrate locally in the developer edition, interacting with models from **Watson XAI** [1]. This means there is no direct remote connection to the main watsonx Orchestrate service in this setup [1].
*   **Visualisation, Debugging & Deployment**: The Flow Builder enables users to visually design their tools, with built-in capabilities to debug their execution and deploy them for agent use [1].
*   **Agent Style Variations**: The demonstration briefly touches on different agent styles (e.g., Default, React) and how they might affect agent reasoning [1].
*   **Enhanced Inspection/Debugging**: A significant highlight is the ability to **directly inspect agent actions and tool invocations**, including looking *inside* code blocks, often facilitated by tools like Langfuse [1]. This is crucial for understanding agent behaviour, especially when debugging unexpected outcomes or prompting issues [1].

## Getting Started: Accessing the Flow Builder

There are two primary ways to access the new Flow Builder functionality:

1.  **Via Tools Menu**:
    *   Navigate to "Agents" [1].
    *   Go to "Tools" [1].
    *   Select "Create a tool" [1].
    *   Choose "Create a new flow" [1].
2.  **During Agent Building**:
    *   When building a new agent, you can select "Add a tool" [1].
    *   From there, choose "Create a new flow" [1].

## Example Walkthrough: The Simple Counter Agent

The video demonstrates building a **"Simple Counter" agent** to showcase the Flow Builder. While not a complex use case, it effectively illustrates the process [1].

*   **Tool Name**: Simple Counter [1].
*   **Input Definition**: The tool expects one input called `counter_input`, which is of type "number" (integer) [1].
*   **Core Logic (Code Block)**:
    *   A code block is inserted into the flow [1].
    *   This block takes the `counter_input` from the overall flow [1].
    *   It then increments this input by one (`+1`) [1].
    *   It defines an output for the code block, named `increment_counter` [1].
*   **Flow Output**: The overall flow also defines an output, `counter_output`, which receives the result from the code block [1]. It's important to note the **two levels of output**: the output from the internal code snippet and the output from the entire flow [1].
*   **Testing and Debugging**:
    *   The agent can be tested directly within the UI preview [1].
    *   The inspection feature (similar to Langfuse) allows detailed viewing of the agent's thought process, tool invocation, and even the internal workings and inputs/outputs of the code blocks [1].
    *   This debugging capability is invaluable for understanding why an agent might produce a certain result, such as identifying if the input passed to the tool was different than expected due to prompting [1].

## Further Insights & Considerations

*   **Rapid Development**: IBM watsonx Orchestrate is undergoing rapid development, and new functionalities like the Flow Builder are frequently introduced [1].
*   **Importance of Descriptions**: When creating tools, providing a **good description** of what the tool does, how the agent should use it, and its parameters is crucial for the agent to correctly select and utilise it [1]. Even with minimal definitions, the tools can still function [1].
*   **Debugging Prompting Issues**: The powerful inspection tools can help diagnose issues related to prompting, for example, if the agent provides an unexpected input value to a tool [1].
*   **Local-First Approach**: The demonstration emphasises working with local AI agents and Watson XAI models, providing a contained environment for development and testing without requiring a direct remote connection to the cloud service [1].
