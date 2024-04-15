# Run GPT_TOD example
## Install the requirements with: 
```pip install -r requirements.txt``` 

## Download Multiwoz Data
```bash download_multiwoz.sh```

## Download gpt_tod model
```
cd model
bash download_bot_model.sh
```

## Add your openai-key in the following file 
```open_ai_key.json```
### or
```azure_openai_key.json```
### The format should be as {"key": "*******"}


## Run the verbose example
```bash verbose_run.sh```

