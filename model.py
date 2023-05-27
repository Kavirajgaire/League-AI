import torch
import numpy as np
from torch import nn
from sklearn.model_selection import train_test_split


class LeagueModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = nn.Linear(in_features=35, out_features=128)
        self.layer_2 = nn.Linear(in_features=128, out_features=64)
        self.layer_3 = nn.Linear(in_features=64, out_features=1)
        self.relu = nn.ReLU()

    def forward(self, x):
        return self.layer_3(self.layer_2(self.relu(self.layer_1(x))))


def accuracy_fn(y_true, y_pred):
    correct = torch.eq(y_true, y_pred).sum().item()
    acc = (correct/len(y_pred)) * 100
    return acc


def train(model: LeagueModel, X: np.array, y: np.array, epochs: int, display=False) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(model.parameters())
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.SGD(params=model.parameters(), lr=0.05)

    X = torch.tensor(X, dtype=torch.float)
    y = torch.tensor(y, dtype=torch.float)
    print(len([i for i in y if i ==0]), len(y))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    X_train, y_train = X_train.to(device), y_train.to(device)
    X_test, y_test = X_test.to(device), y_test.to(device)
    for epoch in range(epochs):
        model.train()

        y_logits = model(X_train).squeeze()
        y_pred = torch.round(torch.sigmoid(y_logits))

        loss = loss_fn(y_logits, y_train)
        acc = accuracy_fn(y_true=y_train, y_pred=y_pred)

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        model.eval()

        with torch.inference_mode():
            test_logits = model(X_test).squeeze()
            test_pred = torch.round(torch.sigmoid(test_logits))

            test_loss = loss_fn(test_logits, y_test)
            test_acc = accuracy_fn(y_true=y_test, y_pred=test_pred)

        if display and epoch % 10 == 0:
            print(f"Epoch: {epoch} | Loss: {loss}, Acc: {acc} | Test loss: {test_loss}, Test acc: {test_acc}")

def main():
    pass

if __name__ == "__main__":
    main()
