#!/usr/bin/env bash
python goal_completion_gpt_4.py --input_file_path  Runs/gpt_4_vanilla.jsonl --output_file_path Results/tod_res_gpt_4_vanilla.jsonl
python goal_completion_gpt_4.py --input_file_path  Runs/ua_gpt3_thought_tod_gpt4_150_350.jsonl --output_file_path Results/tod_res_ua_gpt3_thought_tod_gpt4_150_350.jsonl
