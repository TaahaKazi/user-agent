The 3 files (thought_50.txt, vanilla_50.txt, verbose_50_.txt) contain 50 dialogues each based on the same 50 initial user goals

NOTE: The task completion evaluation (GSR metric) is based solely on the dialogue and ignores the initial user goal.
This is because the user-simulator may sometimes misinterpret or miss user goals from the initial instruction. 
Therefore, the TOD model should be evaluated solely based on the dialogues.

So, when evaluating the dialogues check only if the 'System:' was able to complete the 'User:'s queries.

Scoring rubrics:
Score 0: The model did not complete all the tasks given to it. Even if it completed some tasks but not all mark it as 0
Score 1: The model completed all the tasks given to it

Link to google sheet to store results:
https://docs.google.com/spreadsheets/d/12QJ9Dx9AqPBZQBlwozmQ7sRXkEQRQAD_Flfj4m4mEkE/edit?usp=sharing

Make a copy of the google sheet to annotate


Also, I have added the results from the auto evaluation model (goal_completion_gpt4.log, goal_completion_gpt4_thought.log, goal_completion_gpt4_vanilla.log)
