from app.src.base.base_model import BaseModel
import pathlib
import joblib
import pandas as pd
import sklearn
import torch
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from torch_geometric.nn import SAGEConv, HeteroConv

from app.src.dto.prediction_request import PredictionRequest

def get_model() -> BaseModel:
    return ModelStarter()


class FraudGNN(nn.Module):
    def __init__(self, tx_feature_size, hidden_channels, num_layers):
        super().__init__()
        self.entity_types = ['card', 'addr', 'email', 'device', 'product']
        self.num_layers = num_layers
        self.hidden_channels = hidden_channels

        # Feature projection
        self.tx_proj = nn.Sequential(
            nn.Linear(tx_feature_size, hidden_channels),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_channels, hidden_channels)
        )

        # Entity projection
        self.entity_proj = nn.Sequential(
            nn.Linear(2, hidden_channels),
            nn.ReLU(),
            nn.Dropout(0.2)
        )

        # Convolution layers
        self.convs = nn.ModuleList()
        for i in range(num_layers):
            conv_dict = {}
            for et in self.entity_types:
                conv_dict[('transaction', f'to_{et}', et)] = SAGEConv(
                    hidden_channels, hidden_channels)
                conv_dict[(et, f'from_{et}', 'transaction')] = SAGEConv(
                    hidden_channels, hidden_channels)

            # Add pattern edge convolution
            conv_dict[('transaction', 'tx_pattern', 'transaction')] = SAGEConv(
                hidden_channels, hidden_channels)

            self.convs.append(HeteroConv(conv_dict, aggr='mean'))

        # Prediction head
        self.head = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(hidden_channels, 1)
        )

        # Initialize weights
        self._init_weights()

    def _init_weights(self):
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.kaiming_normal_(module.weight, nonlinearity='relu')
                if module.bias is not None:
                    module.bias.data.zero_()

    def forward(self, data):
        # Project features
        x_dict = {
            'transaction': F.elu(self.tx_proj(data['transaction'].x))
        }

        # Entity features
        for et in self.entity_types:
            if hasattr(data[et], 'x') and data[et].x.size(0) > 0:
                x_dict[et] = self.entity_proj(data[et].x)
            else:
                x_dict[et] = torch.zeros(0, self.entity_proj[0].out_features,
                                         device=data['transaction'].x.device)

        # Message passing
        for conv in self.convs:
            try:
                x_dict = conv(x_dict, data.edge_index_dict)
                x_dict = {k: F.elu(v) for k, v in x_dict.items()}
            except Exception as e:
                continue

        # Final prediction
        return self.head(x_dict['transaction']).squeeze()


class ModelStarter(BaseModel):
    def __init__(self):
        super().__init__("Description of the model")
        path_model = pathlib.Path(__file__).parent.parent / "local_model" / "best_fraud_model.pt"
        path_artifacts = pathlib.Path(__file__).parent.parent / "local_model" / "fraud_inference_artifacts.pkl"
        #path = pathlib.Path(__file__).parent / "local_model" / "wine_quality_model.pkl"
        #print(path)#/app/src/base/local_model/wine_quality_model.pkl
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Load artifacts first to get feature size
        if path_artifacts.exists():
            artifacts = joblib.load(path_artifacts)
            tx_feature_size = artifacts.get('tx_feature_size', 322)  # Default fallback
        else:
            raise Exception('Model doesnt exist')

        if path_model.exists():
            with open(path_model, 'rb') as file:
                self.model = FraudGNN(tx_feature_size, 128, 2).to(device) #joblib.load(file)
                self.model.load_state_dict(torch.load(path_model))
        else:
            raise Exception('Model doesnt exist')

    def predict_result(self, input: PredictionRequest) -> float:
        input_data = input  # чтобы по алиасам! без этого  либо missed поле - когда передавали без пробелов в body или когда передавали с пробелами в body ошибка 500 internal server error
        input_df = pd.DataFrame(input_data, index=[0])
        result = self.model.predict(input_df)[0]
        return result