import torch
import torch.nn as nn
import os


class EmailClassificationModel(nn.Module):
    def __init__(self, input_size):
        super(EmailClassificationModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        res = self.fc1(x)
        res = self.relu(res)
        res = self.fc2(res)
        return res


def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'model.pth')

    model = EmailClassificationModel(input_size=5000)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model
