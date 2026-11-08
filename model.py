import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
data = pd.read_csv(~/Desktop/Python1/My Games/data.csv)
oz = ["player_y","space_height","promijok","vidst_do_trubes","vidst_do_promijok","speed_falldown","flappy_height","flappy_width","truba_width","event"]
goal = "event"
data_oz = data[oz]
data_goal = data[goal]
train_oz, test_oz , train_goal , test_goal = train_test_split(data_oz, data_goal , train_size = 0.6 , random_state = 42 , stratify = data_goal)
model = DecisionTreeClassifier(max_depth = 2, random_state = 42)
model.fit(train_oz , train_goal)
result = model.predict(test_oz)
print(accuracy_score(test_goal,result))