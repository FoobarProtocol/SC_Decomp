#!/usr/bin/env python3

import json
import csv

# Load your JSON
json_data = """
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1694910527,
  "model": "gpt-4-0613",
  "choices": [
      {
          "index": 0,
          "message": {
              "role": "assistant",
              "content": "Sure, here is an example of a synthetic dataset for a machine learning model that aims to predict the output of solidity programming smart contracts:\n\nDataset:\nContract ID | Instruction/Problem                                                      | Input                                       | Correct Output\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n001         | Create a new ERC20 token named \"MyCoin\" with symbol \"MCN\" and 1000 total supply. | \"\", \"\", -1                                  | Error: Invalid inputs\n002         | Transfer 50 \"MyCoin\" from account A to account B.                          | \"MCN\", \"Account A\", \"Account B\", 50         | Success: 50 \"MCN\" transferred from Account A to Account B\n003         | Mint 100 \"MyCoin\" to account C.                                           | \"MCN\", \"Account C\", 100                     | Success: 100 \"MCN\" Minted to Account C\n004         | Burn 30 \"MyCoin\" from account D.                                          | \"MCN\", \"Account D\", 30                      | Success: 30 \"MCN\" Burned from Account D\n005         | Create a new ERC721 token named \"UniqueArt\" with symbol \"UAR\".            | \"UAR\", \"\", -1                               | Error: Invalid inputs\n006         | Transfer 1 \"UniqueArt\" from account A to account B.                       | \"UAR\", \"Account A\", \"Account B\", 1          | Success: 1 \"UAR\" transferred from Account A to Account B\n007         | Mint 1 \"UniqueArt\" to account C.                                          | \"UAR\", \"Account C\", 1                       | Success: 1 \"UAR\" Minted to Account C\n008         | Burn 1 \"UniqueArt\" from account D.                                        | \"UAR\", \"Account D\", 1                       | Success: 1 \"UAR\" Burned from Account D\n009         | Create a new ERC1155 token named \"MixedAsset\" with symbol \"MAS\".          | \"MAS\", \"\", -1                               | Error: Invalid inputs\n010         | Transfer 10 \"MixedAsset\" from account A to account B.                     | \"MAS\", \"Account A\", \"Account B\", 10         | Success: 10 \"MAS\" transferred from Account A to Account B"
          },
          "finish_reason": "stop"
      }
  ],
  "usage": {
      "prompt_tokens": 433,
      "completion_tokens": 475,
      "total_tokens": 908
  }
}
"""
data = json.loads(json_data)

# Extract content
content = data["choices"][0]["message"]["content"]

# Split content into lines
lines = content.split("\n")

# Prepare data for CSV
csv_data = [line.split("|") for line in lines if line.strip()]

# Write data to CSV
with open("output.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_data)
