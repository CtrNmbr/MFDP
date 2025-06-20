from app.src.base.base_model import BaseModel
import pathlib
import joblib
import pandas as pd
import sklearn
import numpy as np
import torch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_sparse
from torch_geometric.data import HeteroData
from torch_geometric.nn import SAGEConv, HeteroConv
from category_encoders import TargetEncoder
from collections import defaultdict
from torch_geometric.loader import NeighborLoader
from sklearn.preprocessing import StandardScaler
import time
from app.src.dto.prediction_request import PredictionRequest
import gc
def get_model() -> BaseModel:
    return ModelStarter()


class FraudFocusedGraphBuilder:
    import gc
    def __init__(self, entity_types, cat_features, inference_mode=False, 
                 target_encoders=None, scaler=None, num_medians=None):
        self.entity_types = entity_types
        self.cat_features = cat_features
        self.transaction_counter = 0
        self.inference_mode = inference_mode
        self.target_encoders = target_encoders
        self.scaler = scaler
        self.num_medians = num_medians
        
        
        self.tx_features = []
        if not self.inference_mode:
            self.tx_labels = []
            self.fraud_indices = []
        self.tx_categorical = {col: [] for col in cat_features}
        self.transaction_ids = []
        self.num_cols = [
            'TransactionAmt','dist1','dist2','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13',
            'C14','D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12','D13','D14','D15','V1','V2','V3','V4',
            'V5','V6','V7','V8','V9','V10','V11','V12','V13','V14','V15','V16','V17','V18','V19','V20','V21','V22','V23',
            'V24','V25','V26','V27','V28','V29','V30','V31','V32','V33','V34','V35','V36','V37','V38','V39','V40','V41',
            'V42','V43','V44','V45','V46','V47','V48','V49','V50','V51','V52','V53','V54','V55','V56','V57','V58','V59',
            'V60','V61','V62','V63','V64','V65','V66','V67','V68','V69','V70','V71','V72','V73','V74','V75','V76','V77',
            'V78','V79','V80','V81','V82','V83','V84','V85','V86','V87','V88','V89','V90','V91','V92','V93','V94','V95',
            'V96','V97','V98','V99','V100','V101','V102','V103','V104','V105','V106','V107','V108','V109','V110','V111',
            'V112','V113','V114','V115','V116','V117','V118','V119','V120','V121','V122','V123','V124','V125','V126',
            'V127','V128','V129','V130','V131','V132','V133','V134','V135','V136','V137','V138','V139','V140','V141',
            'V142','V143','V144','V145','V146','V147','V148','V149','V150','V151','V152','V153','V154','V155','V156',
            'V157','V158','V159','V160','V161','V162','V163','V164','V165','V166','V167','V168','V169','V170','V171',
            'V172','V173','V174','V175','V176','V177','V178','V179','V180','V181','V182','V183','V184','V185','V186',
            'V187','V188','V189','V190','V191','V192','V193','V194','V195','V196','V197','V198','V199','V200','V201',
            'V202','V203','V204','V205','V206','V207','V208','V209','V210','V211','V212','V213','V214','V215','V216',
            'V217','V218','V219','V220','V221','V222','V223','V224','V225','V226','V227','V228','V229','V230','V231',
            'V232','V233','V234','V235','V236','V237','V238','V239','V240','V241','V242','V243','V244','V245','V246',
            'V247','V248','V249','V250','V251','V252','V253','V254','V255','V256','V257','V258','V259','V260','V261',
            'V262','V263','V264','V265','V266','V267','V268','V269','V270','V271','V272','V273','V274','V275','V276',
            'V277','V278','V279','V280','V281','V282','V283','V284','V285','V286','V287','V288','V289','V290','V291',
            'V292','V293','V294','V295','V296','V297','V298','V299','V300','V301','V302','V303','V304','V305','V306',
            'V307','V308','V309','V310','V311','V312','V313','V314','V315','V316','V317','V318','V319','V320','V321',
            'V322','V323','V324','V325','V326','V327','V328','V329','V330','V331','V332','V333','V334','V335','V336',
            'V337','V338','V339','id_01','id_02','id_03','id_04','id_05','id_06','id_07','id_08','id_09','id_10','id_11'
        ]
        
        
        self.entity_maps = {et: {} for et in entity_types}
        self.entity_edges = {et: defaultdict(list) for et in entity_types}
        self.entity_counts = {et: defaultdict(int) for et in entity_types}
        self.fraud_entity_counts = {et: defaultdict(int) for et in entity_types}
        self.train_ratio = 0.8
        
        
        self.pattern_registry = defaultdict(list)
        self.pattern_fraud_counts = defaultdict(int)
        self.pattern_total_counts = defaultdict(int)
        self.amt_bins = [0, 10, 50, 100, 200, 500, 1000, 5000, float('inf')]
        self.non_fraud_patterns = defaultdict(list) if not inference_mode else None

    def get_pattern_key(self, row):
        """Create enhanced pattern key using critical fraud indicators"""
        
        card1 = str(row.get('card1', 'MISSING'))
        card4 = str(row.get('card4', 'MISSING'))  
        card6 = str(row.get('card6', 'MISSING'))  
        
        
        addr1 = str(row.get('addr1', 'MISSING'))
        p_email = str(row.get('P_emaildomain', 'MISSING')).split('.')[0]  
        
        
        device_type = str(row.get('DeviceType', 'MISSING'))
        device_info = str(row.get('DeviceInfo', 'MISSING')).split('_')[0]  
        
        
        product = str(row.get('ProductCD', 'MISSING'))
        m_flags = ''.join(str(row.get(f'M{i}', 'MISSING')) for i in range(1, 10))  
        
        
        amt = row.get('TransactionAmt', 0)
        amt_bin = np.digitize(amt, self.amt_bins, right=False)
        
        return (card1, card4, card6, addr1, p_email, 
                device_type, device_info, product, m_flags, amt_bin)

    def add_batch(self, batch_df):
        start_idx = self.transaction_counter
        end_idx = self.transaction_counter + len(batch_df)
        tx_indices = np.arange(start_idx, end_idx)
        self.transaction_counter = end_idx
        
        
        self.transaction_ids.append(batch_df['TransactionID'].values)
        
        
        features = self.create_features_batch(batch_df)
        self.tx_features.append(features)
        
        if not self.inference_mode:
            labels = batch_df['isFraud'].values
            self.tx_labels.append(labels)
            fraud_mask = (labels == 1)
            if np.any(fraud_mask):
                fraud_indices = tx_indices[fraud_mask]
                self.fraud_indices.extend(fraud_indices)
        
        
        for col in self.cat_features:
            if col in batch_df:
                self.tx_categorical[col].append(batch_df[col].fillna('MISSING').astype(str).values)
            else:
                self.tx_categorical[col].append(np.array(['MISSING'] * len(batch_df)))
        
        
        for et in self.entity_types:
            entities = self.get_entity_values(et, batch_df)
            valid_mask = (entities != '') & (entities != '_') & (entities != '__')
            entities = entities[valid_mask]
            batch_tx_indices = tx_indices[valid_mask]
            
            
            for tx_idx, entity in zip(batch_tx_indices, entities):
                if entity not in self.entity_maps[et]:
                    self.entity_maps[et][entity] = len(self.entity_maps[et])
                entity_idx = self.entity_maps[et][entity]
                self.entity_edges[et][entity_idx].append(tx_idx)
                self.entity_counts[et][entity_idx] += 1
                
                
                if not self.inference_mode and tx_idx in self.fraud_indices:
                    self.fraud_entity_counts[et][entity_idx] += 1
        
        
        for i, (_, row) in enumerate(batch_df.iterrows()):
            pattern_key = self.get_pattern_key(row)
            tx_idx = start_idx + i
            self.pattern_registry[pattern_key].append(tx_idx)
            self.pattern_total_counts[pattern_key] += 1
            
            if not self.inference_mode:
                if row.get('isFraud', 0) == 1:
                    self.pattern_fraud_counts[pattern_key] += 1
                else:
                    self.non_fraud_patterns[pattern_key].append(tx_idx)

    def get_entity_values(self, et, batch_df):
        if et == 'card':
            c1 = batch_df['card1'].fillna('').astype(str).values
            c2 = batch_df['card2'].fillna('').astype(str).values
            c3 = batch_df['card3'].fillna('').astype(str).values
            c4 = batch_df['card4'].fillna('').astype(str).values
            c5 = batch_df['card5'].fillna('').astype(str).values
            c6 = batch_df['card6'].fillna('').astype(str).values
            return c1 + "_" + c2 + "_" + c3 + "_" + c4 + "_" + c5 + "_" + c6
        elif et == 'addr':
            a1 = batch_df['addr1'].fillna('').astype(str).values
            a2 = batch_df['addr2'].fillna('').astype(str).values
            return a1 + "_" + a2
        elif et == 'email':
            p_email = batch_df['P_emaildomain'].fillna('').astype(str).values
            r_email = batch_df['R_emaildomain'].fillna('').astype(str).values
            return p_email + "_" + r_email
        elif et == 'device':
            return batch_df['DeviceInfo'].fillna('').astype(str).values
        elif et == 'product':
            return batch_df['ProductCD'].fillna('').astype(str).values
        return np.array([''] * len(batch_df))
    
    def create_features_batch(self, batch_df):
        """Feature creation with enhanced fraud-specific features"""
        features = []
        
        
        amt = batch_df['TransactionAmt'].values
        features.append(np.log1p(np.where(amt > 0, amt, 0)))
        features.append(np.where(amt > 0, 1, 0))
        
        
        dt = batch_df['TransactionDT'].fillna(0).values
        hour = (dt % 86400) // 3600
        day_of_week = (dt // 86400) % 7
        features.append(np.sin(2 * np.pi * hour / 24))
        features.append(np.cos(2 * np.pi * hour / 24))
        features.append(np.sin(2 * np.pi * day_of_week / 7))
        features.append(np.cos(2 * np.pi * day_of_week / 7))
        
        
        for col in self.num_cols:
            if col in batch_df:
                if self.inference_mode and self.num_medians is not None and col in self.num_medians:
                    median_val = self.num_medians[col]
                else:
                    median_val = batch_df[col].median()
                feat = batch_df[col].fillna(median_val).values.astype(np.float32)
                features.append(feat)
            else:
                features.append(np.zeros(len(batch_df), dtype=np.float32))
        
        return np.column_stack(features)
    
    def apply_target_encoding(self):
        """Apply target encoding with fraud focus"""
        if self.inference_mode:
            cat_data = {}
            for col in self.cat_features:
                cat_data[col] = np.concatenate(self.tx_categorical[col])
            encoded_features = []
            for col in self.cat_features:
                encoded = self.target_encoders[col].transform(cat_data[col]).values.astype(np.float32)
                encoded_features.append(encoded)
            return np.column_stack(encoded_features)
        else:
            
            tx_labels = np.concatenate(self.tx_labels)
            cat_data = {}
            for col in self.cat_features:
                cat_data[col] = np.concatenate(self.tx_categorical[col])
            
            
            num_train = int(self.transaction_counter * self.train_ratio)
            train_mask = np.zeros(self.transaction_counter, dtype=bool)
            train_mask[:num_train] = True
            
            
            self.target_encoders = {}
            encoded_features = []
            for col in self.cat_features:
                
                encoder = TargetEncoder(smoothing=50, min_samples_leaf=100)
                encoder.fit(
                    cat_data[col][train_mask], 
                    tx_labels[train_mask]
                )
                self.target_encoders[col] = encoder
                
                
                encoded = encoder.transform(cat_data[col]).values.astype(np.float32)
                encoded_features.append(encoded)
            
            return np.column_stack(encoded_features)
    
    def build_graph(self):
        print(f"Building optimized fraud-focused graph with {self.transaction_counter} transactions")
        start_time = time.time()
        
        
        num_features = np.vstack(self.tx_features)
        
        
        if not self.inference_mode:
            self.num_medians = {}
            for i, col in enumerate(self.num_cols):
                if i < num_features.shape[1]:
                    self.num_medians[col] = np.median(num_features[:, i])
        
        
        cat_features = self.apply_target_encoding()
        
        
        tx_features = np.hstack([num_features, cat_features])
        
        
        if not self.inference_mode:
            self.scaler = StandardScaler()
            tx_features = self.scaler.fit_transform(tx_features)
        else:
            tx_features = self.scaler.transform(tx_features)
            
        
        pattern_features = np.zeros((tx_features.shape[0], 1), dtype=np.float32)
        for pattern_key, tx_indices in self.pattern_registry.items():
            fraud_count = self.pattern_fraud_counts.get(pattern_key, 0)
            fraud_ratio = fraud_count / len(tx_indices)
            for tx_idx in tx_indices:
                pattern_features[tx_idx] = fraud_ratio
        
        tx_features = np.hstack([tx_features, pattern_features])
        tx_feature_tensor = torch.tensor(tx_features, dtype=torch.float32)
        
        
        data = HeteroData()
        data['transaction'].x = tx_feature_tensor
        
        if not self.inference_mode:
            tx_labels = np.concatenate(self.tx_labels)
            data['transaction'].y = torch.tensor(tx_labels, dtype=torch.float32)
            
            
            num_train = int(self.transaction_counter * self.train_ratio)
            train_mask = torch.zeros(self.transaction_counter, dtype=torch.bool)
            val_mask = torch.zeros(self.transaction_counter, dtype=torch.bool)
            train_mask[:num_train] = True
            val_mask[num_train:] = True
            data['transaction'].train_mask = train_mask
            data['transaction'].val_mask = val_mask
        
        
        if self.inference_mode:
            tx_ids = np.concatenate(self.transaction_ids)
            data['transaction'].transaction_id = torch.tensor(tx_ids, dtype=torch.long)
        
        
        for et in self.entity_types:
            num_entities = len(self.entity_maps[et])
            
            
            entity_features = np.zeros((num_entities, 2), dtype=np.float32)
            for entity_idx in range(num_entities):
                total_count = self.entity_counts[et].get(entity_idx, 0)
                fraud_count = self.fraud_entity_counts[et].get(entity_idx, 0)
                entity_features[entity_idx, 0] = np.log1p(total_count)
                entity_features[entity_idx, 1] = fraud_count / (total_count + 1e-6)  
                
            entity_feature_tensor = torch.tensor(entity_features, dtype=torch.float32)
            data[et].x = entity_feature_tensor
            
            
            src_list, dst_list = [], []
            for entity_idx, tx_indices in self.entity_edges[et].items():
                if entity_idx < num_entities:
                    for tx_idx in tx_indices:
                        src_list.append(tx_idx)
                        dst_list.append(entity_idx)
            
            if src_list:
                edge_index = torch.tensor([src_list, dst_list], dtype=torch.long)
                rev_edge_index = torch.tensor([dst_list, src_list], dtype=torch.long)
            else:
                edge_index = torch.empty((2, 0), dtype=torch.long)
                rev_edge_index = torch.empty((2, 0), dtype=torch.long)
                
            data['transaction', f'to_{et}', et].edge_index = edge_index
            data[et, f'from_{et}', 'transaction'].edge_index = rev_edge_index
        
        
        print("Building pattern-based edges...")
        pattern_edges = set()
        
        
        for pattern_key, tx_indices in self.pattern_registry.items():
            total_count = len(tx_indices)
            
            
            if total_count < 2 or total_count > 500:
                continue
                
            
            for i in range(len(tx_indices)):
                for j in range(i+1, min(i+101, len(tx_indices))):
                    pattern_edges.add((tx_indices[i], tx_indices[j]))
                    pattern_edges.add((tx_indices[j], tx_indices[i]))
        
        if pattern_edges:
            src, dst = zip(*pattern_edges)
            pattern_edge_index = torch.tensor([src, dst], dtype=torch.long)
            data['transaction', 'tx_pattern', 'transaction'].edge_index = pattern_edge_index
            print(f"Added {len(pattern_edges)} pattern-based edges")
        
        
        del self.tx_features, self.entity_edges, self.tx_categorical, self.pattern_registry
        gc.collect()
        
        print(f"Graph built in {time.time()-start_time:.1f} seconds")
        return data


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
        self.path_model = pathlib.Path(__file__).parent.parent / "local_model" / "best_fraud_model6.pt"
        self.path_artifacts = pathlib.Path(__file__).parent.parent / "local_model" / "fraud_inference_artifacts6.pkl"
        #path = pathlib.Path(__file__).parent / "local_model" / "wine_quality_model.pkl"
        #print(path)#/app/src/base/local_model/wine_quality_model.pkl
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        #untimeError: Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False. If you are running 
        #on a CPU-only machine, please use torch.load with map_location=torch.device('cpu') to map your storages to the CPU.
        #This error occurs when you're trying to load a PyTorch model saved on a GPU onto a CPU-only machine. Here's how to resolve it:
        
        # Load artifacts first to get feature size
        if self.path_artifacts.exists():
            self.artifacts = joblib.load(self.path_artifacts)
            self.tx_feature_size = self.artifacts.get('tx_feature_size', 322)  # Default fallback
        else:
            raise Exception('Model doesnt exist')

        if self.path_model.exists():
            with open(self.path_model, 'rb') as file:
                self.model = FraudGNN(self.tx_feature_size, 128, 2).to(self.device) #joblib.load(file)
                self.model.load_state_dict(torch.load(self.path_model, map_location=self.device ))
                #untimeError: Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False. If you are running 
                #on a CPU-only machine, please use torch.load with map_location=torch.device('cpu') to map your storages to the CPU.
                #This error occurs when you're trying to load a PyTorch model saved on a GPU onto a CPU-only machine. Here's how to resolve it:
       
                self.model.eval()
                self.CHUNKSIZE = 100000
                self.ENTITY_TYPES = ['card', 'addr', 'email', 'device', 'product']
                self.CAT_FEATURES = [
                    'ProductCD', 'card1', 'card2', 'card3', 'card4', 'card5', 'card6',
                    'addr1', 'addr2', 'P_emaildomain', 'R_emaildomain',
                    'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9',
                    'DeviceType', 'DeviceInfo'
                ]




        else:
            raise Exception('Model doesnt exist')

    def predict_result(self, input: PredictionRequest) -> float:
        input_data = input  # чтобы по алиасам! без этого  либо missed поле - когда передавали без пробелов в body или когда передавали с пробелами в body ошибка 500 internal server error
        input_df = pd.DataFrame(input_data, index=[0]) # по сути до этого надо было органзиовыввать
        for col in self.CAT_FEATURES + ['card1', 'card2', 'card3', 'card4', 'card5', 'card6',
                   'addr1', 'addr2', 'P_emaildomain', 'R_emaildomain', 
                   'DeviceInfo', 'ProductCD']:
            if col not in input_df:
                input_df[col] = 'MISSING'
        self.graph_builder = FraudFocusedGraphBuilder( # чтобы под каждый батч был свой граф или можно выше чтобы копилось
                    entity_types=self.ENTITY_TYPES,
                    cat_features=self.CAT_FEATURES,
                    inference_mode=True,
                    target_encoders=self.artifacts['target_encoders'],
                    scaler=self.artifacts['scaler'],
                    num_medians=self.artifacts['num_medians']
                )        
        self.graph_builder.add_batch(input_df)
        test_data = self.graph_builder.build_graph()
        test_data = test_data.to(self.device)
        test_loader = NeighborLoader(
        test_data,
        num_neighbors={key: [15, 10] for key in test_data.edge_index_dict},
        input_nodes=('transaction', torch.arange(test_data['transaction'].x.size(0))),
        batch_size=2048,
         shuffle=False
        )
        all_probs = []
        transaction_ids = []
        #test_labels_list = None

        with torch.no_grad():
            for batch in test_loader:
                batch = batch.to(self.device)

                fraud_logits = self.model(batch)
                if fraud_logits.dim() == 0: #IndexError: slice() cannot be applied to a 0-dim tensor.
                    fraud_logits = fraud_logits.unsqueeze(0)  # если скаляр - одна строка а не батч

                seed_logits = fraud_logits[:batch['transaction'].batch_size]
                probs = torch.sigmoid(seed_logits).cpu().numpy()
                all_probs.append(probs)


                seed_ids = batch['transaction'].transaction_id[:batch['transaction'].batch_size].cpu().numpy()
                transaction_ids.append(seed_ids)


        test_probs = np.concatenate(all_probs)
        transaction_ids = np.concatenate(transaction_ids)

        #result = self.model.predict(input_df)[0]
        #submission = pd.DataFrame({
        #'TransactionID': transaction_ids,
        #'isFraud': test_probs
        #})
        return  float(test_probs[0]) # test_probs worker-2       | sqlalchemy.exc.ProgrammingError: (psycopg.ProgrammingError) cannot adapt type 'ndarray' using placeholder '%s' (format: AUTO)       
 #submission не может  №worker-1       | sqlalchemy.exc.ProgrammingError: (psycopg.ProgrammingError) cannot adapt type 'DataFrame' using placeholder '%s' (format: AUTO)     
