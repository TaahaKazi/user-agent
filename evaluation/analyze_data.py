import pandas as pd
import json
import matplotlib.pyplot as plt

# Function to load human evaluation data from JSON
def load_human_eval_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

# Function to load automatic evaluation results from JSON
def load_auto_eval_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    # Convert loaded data into a structured df
    df_list = []
    for conv_id, metrics in data.items():
        metrics_values = [convert_numeric(value) for value in metrics[1:7]]
        df_list.append(pd.DataFrame([metrics_values], index=[conv_id], columns=['Task Completion', 'Naturalness for user simulator', 'Naturalness for TOD system',\
                                                           'Coherence for user simulator', 'Coherence for TOD system', 'Dialogue-level diversity for user simulator']))
    return pd.concat(df_list)

def convert_numeric(value):
    if isinstance(value, str):
        value = value.strip()
        if value.lower() == 'yes':
            return 1
        elif value.lower() == 'no':
            return 0
        elif value.isdigit():
            return int(value)
        else:
            print(value)
    else:
        print(value, type(value))
    return value

def check_type(value, index):
    if not pd.api.types.is_integer(value):
        print(f"Non-integer type found at conv_id {index}: {value} ({type(value)})")


# Load human evaluation data
human_eval_filepath = "./human_eval/human_eval_results.json"
human_eval_data = load_human_eval_data(human_eval_filepath)  # Adjust the filepath as necessary

# Models to process
models = ['verbose', 'vanilla', 'thought']
auto_eval_dir = "../eval_results/"

# Prepare DataFrame for automatic and human data
list_df_auto = []
list_df_human = []

# Load automatic data and prepare DataFrame for both human and automatic data
for model in models:
    auto_data = load_auto_eval_data(auto_eval_dir + f'eval_res_{model}2024-04-21-22-17-35.json')
    for conv_id, row in auto_data.iterrows():
        # print(conv_id, model)
        human_metrics = human_eval_data[model][str(conv_id)]  # Ensure conv_id matches in both datasets
        converted_human_metrics = {k: convert_numeric(v) for k, v in human_metrics.items()}
        list_df_auto.append(auto_data.loc[[conv_id]])
        # df_auto = df_auto.append(pd.DataFrame([metrics], columns=['metric1', 'metric2', 'metric3', 'metric4', 'metric5', 'metric6'], index=[f'{model}-{conv_id}']))
        df_conv_human = pd.DataFrame([list(converted_human_metrics.values())], columns=converted_human_metrics.keys(), index=[conv_id])
        list_df_human.append(df_conv_human)
        # df_human = df_human.append(pd.DataFrame([list(human_metrics.values())], columns=human_metrics.keys(), index=[f'{model}-{conv_id}']))

df_auto = pd.concat(list_df_auto)
df_human = pd.concat(list_df_human)


""" print("First few rows of df_human:")
#print(df_human.to_string())  # Shows the first 5 entries

print("First few rows of df_auto:")
#print(df_auto.to_string())  # Shows the first 5 entries

# Print the size of each DataFrame
print("\nSize of df_human:", df_human.shape)  # (number of rows, number of columns)
print("Size of df_auto:", df_auto.shape)

# Print data types of the columns in each DataFrame
print("\nData types in df_human:")
print(df_human.dtypes)

print("Data types in df_auto:")
print(df_auto.dtypes)

df_human['Task Completion'].apply(check_type, args=(df_human.index,))

 """
# Calculate correlation coefficient for each metric
# Pearson correlation coefficient
correlations1 = df_human.corrwith(df_auto)
print("Pearson correlation coefficient")
print(correlations1)

correlations2 = df_human.corrwith(df_auto, method='kendall')
print("Kendall correlation coefficient")
print(correlations2)

correlations3 = df_human.corrwith(df_auto, method="spearman")
print("Spearman correlation coefficient")
print(correlations3)

# Plotting correlations
""" correlations.plot(kind='bar')
plt.title('Correlation between Human and Automatic Evaluations')
plt.xlabel('Metric')
plt.ylabel('Pearson Correlation Coefficient')
plt.tight_layout()
plt.show()
 """
# Export to CSV
df_human.to_csv('human_evaluation_results.csv')
df_auto.to_csv('automatic_evaluation_results.csv')

