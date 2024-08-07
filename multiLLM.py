# python3 multiLLM.py "tell me about space [Prompt]"
# Install:
# ollama run gemma2
# ollama run phi3
# ollama run mistral
# ollama run mathstral
# ollama run llama3.1
# Description:
# This script leverages multiple LLMs to work together to generate and refine a summary
# based on a given prompt. By using specialized models for different roles, it combines their responses through
# iterative rounds to produce a final summary.
# Models in Use:
# - gemma2: Fact Provider
# - mistral: Context Explainer
# - llama3.1: Implications Analyzer
# - phi3: Summarizer
# - mathstral: Mathematical Contextualizer
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_community.llms import Ollama
import numpy as np
import argparse
def runModel(modelName, prompt):
    llm = Ollama(model=modelName)
    response = llm.invoke(prompt)
    return modelName, response
def evalResponse(response):
    lengthScore = len(response.split())
    keywordRelevance = response.lower().count("sky")
    score = lengthScore + keywordRelevance
    return score
def teamSummary(prompt, rounds=3):
    models = {"gemma2": {"role": "Fact Provider", "weight": 1.0}, "mistral": {"role": "Context Explainer", "weight": 1.0}, "llama3.1": {"role": "Implications Analyzer", "weight": 1.0}, "phi3": {"role": "Summarizer", "weight": 1.0}, "mathstral": {"role": "Mathematical Contextualizer", "weight": 1.0}}
    combinedPrompt = prompt
    for roundNum in range(rounds):
        print(f"Round {roundNum + 1}")
        responses = {}
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(runModel, model, combinedPrompt): model for model in models}
            for future in as_completed(futures):
                modelName, response = future.result()
                responses[modelName] = response
                print(f"Response from {modelName} ({models[modelName]['role']}): {response}")
        for model in models:
            score = evalResponse(responses[model])
            models[model]['weight'] = max(score, 0.1)
        combinedResponses = " ".join(f"({models[model]['role']} - Weight: {models[model]['weight']}): {response}"
                                      for model, response in responses.items())
        combinedPrompt = f"Summarize and improve the following responses, considering their roles: {combinedResponses}"
    summarizingModel = "phi3"
    llm = Ollama(model=summarizingModel)
    finalSummary = llm.invoke(combinedPrompt)
    return finalSummary
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pooled Ai")
    parser.add_argument("prompt", type=str, help="The prompt for pooled Ai")
    args = parser.parse_args()
    finalSummary = teamSummary(args.prompt)
    print(f"Final Summary: {finalSummary}")