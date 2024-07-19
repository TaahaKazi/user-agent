#!/usr/bin/env bash
python goal_completion_gpt_4.py --input_file_path  Runs/ua_gpt3_thought_tod_gpt32024-06-05-20-41-23.jsonl --output_file_path Results/tod_res_ua_gpt3_thought_tod_gpt32024-06-05-20-41-23.jsonl
python goal_completion_gpt_4.py --input_file_path  Runs/ua_gpt3_vanilla_tod_gpt32024-06-05-19-43-15.jsonl --output_file_path Results/tod_res_ua_gpt3_vanilla_tod_gpt32024-06-05-19-43-15.jsonl
python goal_completion_gpt_4.py --input_file_path  Runs/ua_gpt3_verbose_tod_gpt32024-06-05-22-12-03.jsonl --output_file_path Results/tod_res_ua_gpt3_verbose_tod_gpt32024-06-05-22-12-03.jsonl